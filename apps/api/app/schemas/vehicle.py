from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VehicleListingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    make: str
    model: str
    year: int
    mileage: int
    condition: str
    transmission: str
    fuel_type: str
    body_type: str
    location: str
    description: str
    price: Decimal
    currency: str
    image_url: str
    stock: int
    status: str
    created_at: datetime
