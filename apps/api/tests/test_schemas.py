import pytest
from pydantic import ValidationError

from app.schemas.order import OrderCreate


def test_order_quantity_cannot_exceed_unique_vehicle_stock() -> None:
    with pytest.raises(ValidationError):
        OrderCreate.model_validate(
            {
                "items": [
                    {"vehicle_listing_id": "10000000-0000-4000-8000-000000000001", "quantity": 2}
                ]
            }
        )


def test_order_requires_at_least_one_vehicle() -> None:
    with pytest.raises(ValidationError):
        OrderCreate.model_validate({"items": []})
