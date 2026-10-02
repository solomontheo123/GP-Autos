from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    vehicle_listing_id: UUID
    quantity: int = Field(ge=1, le=1)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1, max_length=10)


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vehicle_listing_id: UUID
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    vehicle_listing: VehicleOrderRead


class VehicleOrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str
    image_url: str


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    subtotal: Decimal
    total: Decimal
    currency: str
    customer_email: str
    payment_reference: str | None
    payment_status: str
    created_at: datetime
    items: list[OrderItemRead]
