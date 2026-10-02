import hashlib
import hmac
from decimal import Decimal
from uuid import UUID

import httpx
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.enums import ListingStatus, OrderStatus, PaymentStatus
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.vehicle import VehicleListing
from app.services.email_service import send_order_confirmation


async def initialize_payment(
    session: AsyncSession, order_id: UUID, user_id: UUID
) -> tuple[str, str]:
    if session.in_transaction():
        await session.commit()
    async with session.begin():
        order = await session.scalar(select(Order).where(Order.id == order_id).with_for_update())
        if order is None or order.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        if order.status != OrderStatus.PENDING or order.payment_status != PaymentStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Order is not awaiting payment"
            )
        if not settings.paystack_secret_key.get_secret_value():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Payment service is not configured",
            )
        if not order.payment_reference:
            order.payment_reference = f"gp_{order.id.hex}"
        reference = order.payment_reference
        amount_kobo = int((Decimal(order.total) * 100).quantize(Decimal("1")))
        email = order.customer_email

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            f"{settings.paystack_base_url.rstrip('/')}/transaction/initialize",
            headers={"Authorization": f"Bearer {settings.paystack_secret_key.get_secret_value()}"},
            json={
                "email": email,
                "amount": amount_kobo,
                "currency": "NGN",
                "reference": reference,
                "callback_url": settings.paystack_callback_url,
                "metadata": {"order_id": str(order_id)},
            },
        )
        response.raise_for_status()
        payload = response.json()
    if not payload.get("status") or not isinstance(payload.get("data"), dict):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Payment initialization failed"
        )
    authorization_url = payload["data"].get("authorization_url")
    if not isinstance(authorization_url, str):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Payment provider returned no authorization URL",
        )
    return authorization_url, reference


async def _fetch_verified_transaction(reference: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            f"{settings.paystack_base_url.rstrip('/')}/transaction/verify/{reference}",
            headers={"Authorization": f"Bearer {settings.paystack_secret_key.get_secret_value()}"},
        )
        response.raise_for_status()
        payload = response.json()
    data = payload.get("data")
    if not payload.get("status") or not isinstance(data, dict):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Payment verification failed"
        )
    return data


async def apply_verified_payment(
    session: AsyncSession, reference: str, transaction: dict[str, object]
) -> Order:
    async with session.begin():
        order = await session.scalar(
            select(Order)
            .where(Order.payment_reference == reference)
            .options(
                selectinload(Order.items).selectinload(OrderItem.vehicle_listing),
                selectinload(Order.user),
            )
            .with_for_update()
        )
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Payment order not found"
            )
        expected_amount = int((Decimal(order.total) * 100).quantize(Decimal("1")))
        details_match = (
            transaction.get("reference") == reference
            and transaction.get("amount") == expected_amount
            and transaction.get("currency") == order.currency
        )
        if not details_match:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Payment details did not match this order",
            )
        if transaction.get("status") != "success":
            if order.status != OrderStatus.PAID:
                order.payment_status = PaymentStatus.FAILED
                order.status = OrderStatus.FAILED
                for item in order.items:
                    listing = await session.scalar(
                        select(VehicleListing)
                        .where(VehicleListing.id == item.vehicle_listing_id)
                        .with_for_update()
                    )
                    if listing is not None:
                        listing.stock += item.quantity
                        if listing.status == ListingStatus.RESERVED:
                            listing.status = ListingStatus.ACTIVE
        elif order.status != OrderStatus.PAID:
            order.payment_status = PaymentStatus.SUCCESS
            order.status = OrderStatus.PAID
            for item in order.items:
                listing = await session.scalar(
                    select(VehicleListing)
                    .where(VehicleListing.id == item.vehicle_listing_id)
                    .with_for_update()
                )
                if listing is not None and listing.stock == 0:
                    listing.status = ListingStatus.SOLD
        await session.flush()

    order = await session.scalar(
        select(Order)
        .where(Order.id == order.id)
        .options(
            selectinload(Order.items).selectinload(OrderItem.vehicle_listing),
            selectinload(Order.user),
        )
    )
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    await session.commit()
    if order.status == OrderStatus.PAID and order.confirmation_email_sent_at is None:
        await send_order_confirmation(session, order)
    return order


async def verify_payment(session: AsyncSession, reference: str, user_id: UUID) -> Order:
    if not settings.paystack_secret_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment service is not configured",
        )
    if session.in_transaction():
        await session.commit()
    order = await session.scalar(
        select(Order).where(Order.payment_reference == reference, Order.user_id == user_id)
    )
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment order not found")
    await session.commit()
    transaction = await _fetch_verified_transaction(reference)
    return await apply_verified_payment(session, reference, transaction)


def verify_webhook_signature(raw_body: bytes, signature: str | None) -> bool:
    secret = settings.paystack_secret_key.get_secret_value()
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha512).hexdigest()
    return hmac.compare_digest(expected, signature)


async def process_webhook_event(session: AsyncSession, event: dict[str, object]) -> Order | None:
    if event.get("event") != "charge.success":
        return None
    data = event.get("data")
    if not isinstance(data, dict):
        return None
    reference = data.get("reference")
    if not isinstance(reference, str):
        return None
    verified = await _fetch_verified_transaction(reference)
    return await apply_verified_payment(session, reference, verified)
