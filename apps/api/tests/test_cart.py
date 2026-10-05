import pytest
from pydantic import ValidationError

from app.schemas.cart import CartItemCreate


def test_cart_item_quantity_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        CartItemCreate.model_validate({
            "vehicle_listing_id": "10000000-0000-4000-8000-000000000001",
            "quantity": 0,
        })


def test_cart_item_quantity_cannot_exceed_one() -> None:
    with pytest.raises(ValidationError):
        CartItemCreate.model_validate({
            "vehicle_listing_id": "10000000-0000-4000-8000-000000000001",
            "quantity": 2,
        })
