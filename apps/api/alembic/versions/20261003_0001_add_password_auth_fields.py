"""Add password auth support to users.

Revision ID: 20261003_0001
Revises: 20261001_0001
Create Date: 2026-10-03
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261003_0001"
down_revision: str | Sequence[str] | None = "20261001_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("users", "google_id", existing_type=sa.String(length=255), nullable=True)
    op.add_column("users", sa.Column("password_hash", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "password_hash")
    op.alter_column("users", "google_id", existing_type=sa.String(length=255), nullable=False)
