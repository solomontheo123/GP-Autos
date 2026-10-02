from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import ListingStatus, OrderStatus, PaymentStatus
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.vehicle import VehicleListing
from app.schemas.order import OrderCreate


async def create_order(session: AsyncSession, user: User, payload: OrderCreate) -> Order:
    requested_ids = [item.vehicle_listing_id for item in payload.items]
    if len(set(requested_ids)) != len(requested_ids):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Each vehicle can appear only once",
        )

    if session.in_transaction():
        await session.commit()
    async with session.begin():
        result = await session.scalars(
            select(VehicleListing)
            .where(VehicleListing.id.in_(requested_ids))
            .order_by(VehicleListing.id)
            .with_for_update()
        )
        listings = {listing.id: listing for listing in result}
        if len(listings) != len(requested_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="One or more vehicles were not found"
            )

        subtotal = Decimal("0.00")
        items: list[OrderItem] = []
        for requested in payload.items:
            listing = listings[requested.vehicle_listing_id]
            if listing.status != ListingStatus.ACTIVE or listing.stock < requested.quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"{listing.title} is no longer available",
                )
            listing.stock -= requested.quantity
            if listing.stock == 0:
                listing.status = ListingStatus.RESERVED
            line_total = listing.price * requested.quantity
            subtotal += line_total
            items.append(
                OrderItem(
                    vehicle_listing_id=listing.id,
                    quantity=requested.quantity,
                    unit_price=listing.price,
                    subtotal=line_total,
                )
            )

        order = Order(
            user_id=user.id,
            status=OrderStatus.PENDING,
            subtotal=subtotal,
            total=subtotal,
            currency="NGN",
            customer_email=user.email,
            payment_status=PaymentStatus.PENDING,
            items=items,
        )
        session.add(order)
        await session.flush()
        await session.refresh(order, attribute_names=["items"])
    created_order = await session.scalar(
        select(Order)
        .where(Order.id == order.id)
        .options(selectinload(Order.items).selectinload(OrderItem.vehicle_listing))
    )
    if created_order is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Order could not be loaded"
        )
    return created_order


async def get_order_for_user(session: AsyncSession, order_id: UUID, user: User) -> Order | None:
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.vehicle_listing))
        .where(Order.id == order_id, Order.user_id == user.id)
    )
    return result.scalar_one_or_none()


async def list_orders_for_user(session: AsyncSession, user: User) -> list[Order]:
    result = await session.scalars(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.vehicle_listing))
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
    )
    return list(result)
