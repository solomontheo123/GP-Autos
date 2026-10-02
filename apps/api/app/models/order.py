from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import OrderStatus, PaymentStatus

if TYPE_CHECKING:
    from app.models.order_item import OrderItem
    from app.models.user import User


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="ck_orders_subtotal_nonnegative"),
        CheckConstraint("total >= 0", name="ck_orders_total_nonnegative"),
        Index("ix_orders_user_created", "user_id", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(
            OrderStatus,
            values_callable=lambda enum: [member.value for member in enum],
            name="order_status",
        ),
        default=OrderStatus.PENDING,
    )
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(3), default="NGN")
    customer_email: Mapped[str] = mapped_column(String(320))
    payment_reference: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(
            PaymentStatus,
            values_callable=lambda enum: [member.value for member in enum],
            name="payment_status",
        ),
        default=PaymentStatus.PENDING,
    )
    confirmation_email_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    user: Mapped[User] = relationship(back_populates="orders")
    items: Mapped[list[OrderItem]] = relationship(
        back_populates="order", cascade="all, delete-orphan", lazy="selectin"
    )
