import json

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.payment import (
    PaymentInitializeRequest,
    PaymentInitializeResponse,
    PaymentVerifyResponse,
)
from app.services.payment_service import (
    initialize_payment,
    process_webhook_event,
    verify_payment,
    verify_webhook_signature,
)

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.post("/initialize", response_model=PaymentInitializeResponse)
async def post_initialize_payment(
    payload: PaymentInitializeRequest,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PaymentInitializeResponse:
    authorization_url, reference = await initialize_payment(session, payload.order_id, user.id)
    await session.commit()
    return PaymentInitializeResponse(authorization_url=authorization_url, reference=reference)


@router.get("/verify/{reference}", response_model=PaymentVerifyResponse)
async def get_verify_payment(
    reference: str,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PaymentVerifyResponse:
    order = await verify_payment(session, reference, user.id)
    await session.commit()
    return PaymentVerifyResponse(
        order_id=order.id,
        order_status=order.status.value,
        payment_status=order.payment_status.value,
    )


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def paystack_webhook(
    request: Request, session: AsyncSession = Depends(get_session)
) -> Response:
    raw_body = await request.body()
    signature = request.headers.get("x-paystack-signature")
    if not verify_webhook_signature(raw_body, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook signature"
        )
    try:
        event = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload"
        ) from None
    if not isinstance(event, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload"
        )
    await process_webhook_event(session, event)
    await session.commit()
    return Response(status_code=status.HTTP_200_OK)
