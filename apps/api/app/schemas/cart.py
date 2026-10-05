from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CartItemCreate(BaseModel):
    vehicle_listing_id: UUID
    quantity: int = Field(default=1, ge=1, le=1)


class VehicleCartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    make: str
    model: str
    year: int
    mileage: int
    location: str
    price: Decimal
    currency: str
    image_url: str


class CartItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    vehicle_listing_id: UUID
    quantity: int
    created_at: datetime
    vehicle_listing: VehicleCartRead
