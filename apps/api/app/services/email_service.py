from datetime import UTC, datetime
from decimal import Decimal
from html import escape

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.order import Order
from app.models.order_item import OrderItem


def _format_naira(amount: Decimal) -> str:
    return f"NGN {amount:,.0f}"


async def send_order_confirmation(session: AsyncSession, order: Order) -> bool:
    if session.in_transaction():
        await session.commit()
    async with session.begin():
        locked_order = await session.scalar(
            select(Order)
            .where(Order.id == order.id)
            .options(
                selectinload(Order.items).selectinload(OrderItem.vehicle_listing),
                selectinload(Order.user),
            )
            .with_for_update()
        )
        if locked_order is None:
            return False
        if locked_order.confirmation_email_sent_at is not None:
            return True
        if not settings.mailgun_api_key.get_secret_value() or not settings.mailgun_domain:
            return False

        item_rows = "".join(
            f"<li>{escape(item.vehicle_listing.title)} — {item.quantity} × "
            f"{_format_naira(item.unit_price)}</li>"
            for item in locked_order.items
        )
        text_rows = "\n".join(
            f"- {item.vehicle_listing.title}: {item.quantity} × {_format_naira(item.unit_price)}"
            for item in locked_order.items
        )
        order_id = str(locked_order.id)
        reference = locked_order.payment_reference or "Not available"
        total = _format_naira(locked_order.total)
        customer_name = escape(locked_order.user.name)
        html = (
            "<h1>GP AUTOS</h1><h2>Order Confirmation</h2>"
            f"<p>Hello {customer_name}, your payment has been verified.</p>"
            f"<p>Order ID: {order_id}<br>Payment reference: {escape(reference)}</p>"
            f"<ul>{item_rows}</ul><p>Total: <strong>{total}</strong></p>"
            f"<p>Payment status: {escape(locked_order.payment_status.value)}</p>"
        )
        text = (
            "GP AUTOS — Order Confirmation\n\n"
            f"Customer: {locked_order.user.name}\nOrder ID: {order_id}\n"
            f"Payment reference: {reference}\n"
            f"{text_rows}\nTotal: {total}\nPayment status: {locked_order.payment_status.value}\n"
            f"Date: {datetime.now(UTC).isoformat()}"
        )
        base_url = settings.mailgun_base_url.rstrip("/")
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                f"{base_url}/v3/{settings.mailgun_domain}/messages",
                auth=("api", settings.mailgun_api_key.get_secret_value()),
                data={
                    "from": settings.mailgun_from_email,
                    "to": locked_order.customer_email,
                    "subject": f"GP Autos order confirmation {order_id[:8]}",
                    "text": text,
                    "html": html,
                },
            )
            response.raise_for_status()
        locked_order.confirmation_email_sent_at = datetime.now(UTC)
    return True
