from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead
from app.services.order_service import create_order, get_order_for_user, list_orders_for_user

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def post_order(
    payload: OrderCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> OrderRead:
    order = await create_order(session, user, payload)
    await session.commit()
    return OrderRead.model_validate(order)


@router.get("", response_model=list[OrderRead])
async def read_orders(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[OrderRead]:
    return [OrderRead.model_validate(order) for order in await list_orders_for_user(session, user)]


@router.get("/{order_id}", response_model=OrderRead)
async def read_order(
    order_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> OrderRead:
    order = await get_order_for_user(session, order_id, user)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return OrderRead.model_validate(order)
