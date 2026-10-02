"""Create GP Autos marketplace tables.

Revision ID: 20261001_0001
Revises:
Create Date: 2026-10-01
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "20261001_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

listing_status = postgresql.ENUM(
    "active", "reserved", "sold", "inactive", name="listing_status", create_type=False
)
order_status = postgresql.ENUM(
    "pending", "paid", "failed", "cancelled", name="order_status", create_type=False
)
payment_status = postgresql.ENUM(
    "pending", "success", "failed", name="payment_status", create_type=False
)


def upgrade() -> None:
    bind = op.get_bind()
    listing_status.create(bind, checkfirst=True)
    order_status.create(bind, checkfirst=True)
    payment_status.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("google_id", sa.String(255), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("avatar_url", sa.String(2048)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("google_id", name="uq_users_google_id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_google_id", "users", ["google_id"])
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "vehicle_listings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "seller_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("make", sa.String(100), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("mileage", sa.Integer(), nullable=False),
        sa.Column("condition", sa.String(50), nullable=False),
        sa.Column("transmission", sa.String(50), nullable=False),
        sa.Column("fuel_type", sa.String(50), nullable=False),
        sa.Column("body_type", sa.String(50), nullable=False),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Numeric(14, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default="NGN"),
        sa.Column("image_url", sa.String(2048), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", listing_status, nullable=False, server_default="active"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("price > 0", name="ck_vehicle_listings_price_positive"),
        sa.CheckConstraint("stock >= 0", name="ck_vehicle_listings_stock_nonnegative"),
        sa.UniqueConstraint("slug", name="uq_vehicle_listings_slug"),
    )
    op.create_index("ix_vehicle_listings_slug", "vehicle_listings", ["slug"])
    op.create_index("ix_vehicle_listings_make", "vehicle_listings", ["make"])
    op.create_index("ix_vehicle_listings_model", "vehicle_listings", ["model"])
    op.create_index("ix_vehicle_listings_location", "vehicle_listings", ["location"])
    op.create_index(
        "ix_vehicle_listings_active_created", "vehicle_listings", ["status", "created_at"]
    )

    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("status", order_status, nullable=False, server_default="pending"),
        sa.Column("subtotal", sa.Numeric(14, 2), nullable=False),
        sa.Column("total", sa.Numeric(14, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default="NGN"),
        sa.Column("customer_email", sa.String(320), nullable=False),
        sa.Column("payment_reference", sa.String(100)),
        sa.Column("payment_status", payment_status, nullable=False, server_default="pending"),
        sa.Column("confirmation_email_sent_at", sa.DateTime(timezone=True)),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("subtotal >= 0", name="ck_orders_subtotal_nonnegative"),
        sa.CheckConstraint("total >= 0", name="ck_orders_total_nonnegative"),
        sa.UniqueConstraint("payment_reference", name="uq_orders_payment_reference"),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"])
    op.create_index("ix_orders_user_created", "orders", ["user_id", "created_at"])

    op.create_table(
        "order_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "order_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("orders.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "vehicle_listing_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("vehicle_listings.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(14, 2), nullable=False),
        sa.Column("subtotal", sa.Numeric(14, 2), nullable=False),
        sa.CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),
        sa.CheckConstraint("unit_price > 0", name="ck_order_items_unit_price_positive"),
    )
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_vehicle_listing_id", "order_items", ["vehicle_listing_id"])


def downgrade() -> None:
    op.drop_index("ix_order_items_vehicle_listing_id", table_name="order_items")
    op.drop_index("ix_order_items_order_id", table_name="order_items")
    op.drop_table("order_items")
    op.drop_index("ix_orders_user_created", table_name="orders")
    op.drop_index("ix_orders_user_id", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_vehicle_listings_active_created", table_name="vehicle_listings")
    op.drop_index("ix_vehicle_listings_location", table_name="vehicle_listings")
    op.drop_index("ix_vehicle_listings_model", table_name="vehicle_listings")
    op.drop_index("ix_vehicle_listings_make", table_name="vehicle_listings")
    op.drop_index("ix_vehicle_listings_slug", table_name="vehicle_listings")
    op.drop_table("vehicle_listings")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_google_id", table_name="users")
    op.drop_table("users")
    payment_status.drop(op.get_bind(), checkfirst=True)
    order_status.drop(op.get_bind(), checkfirst=True)
    listing_status.drop(op.get_bind(), checkfirst=True)
