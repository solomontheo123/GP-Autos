from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ListingStatus

if TYPE_CHECKING:
    from app.models.cart_item import CartItem
    from app.models.order_item import OrderItem


class VehicleListing(Base):
    __tablename__ = "vehicle_listings"
    __table_args__ = (
        CheckConstraint("price > 0", name="ck_vehicle_listings_price_positive"),
        CheckConstraint("stock >= 0", name="ck_vehicle_listings_stock_nonnegative"),
        Index("ix_vehicle_listings_active_created", "status", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    seller_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    make: Mapped[str] = mapped_column(String(100), index=True)
    model: Mapped[str] = mapped_column(String(100), index=True)
    year: Mapped[int] = mapped_column(Integer)
    mileage: Mapped[int] = mapped_column(Integer)
    condition: Mapped[str] = mapped_column(String(50))
    transmission: Mapped[str] = mapped_column(String(50))
    fuel_type: Mapped[str] = mapped_column(String(50))
    body_type: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="NGN")
    image_url: Mapped[str] = mapped_column(String(2048))
    stock: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[ListingStatus] = mapped_column(
        Enum(
            ListingStatus,
            values_callable=lambda enum: [member.value for member in enum],
            name="listing_status",
        ),
        default=ListingStatus.ACTIVE,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    order_items: Mapped[list[OrderItem]] = relationship(back_populates="vehicle_listing")
    cart_items: Mapped[list[CartItem]] = relationship(back_populates="vehicle_listing")
