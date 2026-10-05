from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemRead
from app.services.cart_service import add_item_to_cart, clear_cart, list_cart_items_for_user, remove_item_from_cart

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("", response_model=list[CartItemRead])
async def read_cart(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list[CartItemRead]:
    cart_items = await list_cart_items_for_user(session, user)
    return [CartItemRead.model_validate(item) for item in cart_items]


@router.post("/items", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
async def add_cart_item(
    payload: CartItemCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> CartItemRead:
    item = await add_item_to_cart(session, user, payload)
    await session.commit()
    return CartItemRead.model_validate(item)


@router.delete("/items/{vehicle_listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    vehicle_listing_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Response:
    deleted = await remove_item_from_cart(session, user, vehicle_listing_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found",
        )
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Response:
    await clear_cart(session, user)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
