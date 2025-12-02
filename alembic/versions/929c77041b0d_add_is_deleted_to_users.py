"""add is_deleted to users

Revision ID: 929c77041b0d
Revises: 0fd1c7063ecc
Create Date: 2025-12-02 11:27:55.672008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '929c77041b0d'
down_revision: Union[str, Sequence[str], None] = '0fd1c7063ecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     """Upgrade schema."""
#     pass


# def downgrade() -> None:
#     """Downgrade schema."""
#     pass

def upgrade():
    op.add_column(
        "users",
        sa.Column("is_deleted", sa.Boolean(), server_default="false", nullable=False)
    )

def downgrade():
    op.drop_column("users", "is_deleted")