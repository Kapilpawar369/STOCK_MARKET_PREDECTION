"""add name column to users

Revision ID: 260266d03e39
Revises: 929c77041b0d
Create Date: 2025-12-02 11:39:43.156324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '260266d03e39'
down_revision: Union[str, Sequence[str], None] = '929c77041b0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     """Upgrade schema."""
#     pass


# def downgrade() -> None:
#     """Downgrade schema."""
#     pass

def upgrade():
    op.add_column("users", sa.Column("name", sa.String(), nullable=True))

def downgrade():
    op.drop_column("users", "name")
