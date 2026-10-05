"""Add cart items table.

Revision ID: 20261003_0002
Revises: 20261003_0001
Create Date: 2026-10-03
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "20261003_0002"
down_revision: str | Sequence[str] | None = "20261003_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "cart_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "vehicle_listing_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("vehicle_listings.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("quantity > 0", name="ck_cart_items_quantity_positive"),
        sa.UniqueConstraint("user_id", "vehicle_listing_id", name="uq_cart_items_user_vehicle"),
    )
    op.create_index("ix_cart_items_user_id", "cart_items", ["user_id"])
    op.create_index("ix_cart_items_vehicle_listing_id", "cart_items", ["vehicle_listing_id"])


def downgrade() -> None:
    op.drop_index("ix_cart_items_vehicle_listing_id", table_name="cart_items")
    op.drop_index("ix_cart_items_user_id", table_name="cart_items")
    op.drop_table("cart_items")
