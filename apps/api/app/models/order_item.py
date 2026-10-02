from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.order import Order
from app.models.vehicle import VehicleListing


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),
        CheckConstraint("unit_price > 0", name="ck_order_items_unit_price_positive"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    vehicle_listing_id: Mapped[UUID] = mapped_column(
        ForeignKey("vehicle_listings.id", ondelete="RESTRICT"), index=True
    )
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    order: Mapped[Order] = relationship(back_populates="items")
    vehicle_listing: Mapped[VehicleListing] = relationship(back_populates="order_items")
