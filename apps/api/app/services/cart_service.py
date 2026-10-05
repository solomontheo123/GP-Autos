from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart_item import CartItem
from app.models.user import User
from app.models.vehicle import VehicleListing
from app.schemas.cart import CartItemCreate


async def list_cart_items_for_user(session: AsyncSession, user: User) -> list[CartItem]:
    result = await session.scalars(
        select(CartItem)
        .where(CartItem.user_id == user.id)
        .options(selectinload(CartItem.vehicle_listing))
        .order_by(CartItem.created_at.desc())
    )
    return list(result)


async def add_item_to_cart(
    session: AsyncSession,
    user: User,
    payload: CartItemCreate,
) -> CartItem:
    listing = await session.scalar(select(VehicleListing).where(VehicleListing.id == payload.vehicle_listing_id))
    if listing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle listing not found",
        )
    if listing.status.value != "active" or listing.stock <= 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This vehicle is no longer available to add to cart.",
        )

    existing = await session.scalar(
        select(CartItem)
        .where(
            CartItem.user_id == user.id,
            CartItem.vehicle_listing_id == payload.vehicle_listing_id,
        )
        .options(selectinload(CartItem.vehicle_listing))
    )
    if existing is not None:
        return existing

    cart_item = CartItem(
        user_id=user.id,
        vehicle_listing_id=payload.vehicle_listing_id,
        quantity=payload.quantity,
    )
    session.add(cart_item)
    await session.flush()
    await session.refresh(cart_item, attribute_names=["vehicle_listing"])
    return cart_item


async def remove_item_from_cart(
    session: AsyncSession,
    user: User,
    vehicle_listing_id: UUID,
) -> bool:
    result = await session.execute(
        select(CartItem).where(
            CartItem.user_id == user.id,
            CartItem.vehicle_listing_id == vehicle_listing_id,
        )
    )
    item = result.scalar_one_or_none()
    if item is None:
        return False
    await session.delete(item)
    return True


async def clear_cart(session: AsyncSession, user: User) -> None:
    await session.execute(delete(CartItem).where(CartItem.user_id == user.id))
