"""add razorpay fields to payments

Revision ID: 06985125a454
Revises: d477c45434b9
Create Date: 2025-11-27 15:27:56.562882
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '06985125a454'
down_revision: Union[str, Sequence[str], None] = 'd477c45434b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ✅ 1. CREATE ENUM FIRST
    payment_status_enum = sa.Enum(
        'CREATED', 'SUCCESS', 'FAILED',
        name='paymentstatus'
    )
    payment_status_enum.create(op.get_bind(), checkfirst=True)

    # ✅ 2. ADD NEW RAZORPAY FIELDS
    op.add_column('payments', sa.Column('provider', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('provider_order_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('provider_payment_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('provider_signature', sa.String(), nullable=True))
    op.add_column(
        'payments',
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'),
                  nullable=True)
    )

    # ✅ 3. MAKE EXISTING FIELDS NOT NULL
    op.alter_column(
        'payments',
        'amount',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False
    )

    op.alter_column(
        'payments',
        'currency',
        existing_type=sa.VARCHAR(),
        nullable=False
    )

    # ✅ 4. SAFELY CONVERT VARCHAR → ENUM
    op.execute(
        "ALTER TABLE payments "
        "ALTER COLUMN status TYPE paymentstatus "
        "USING status::paymentstatus"
    )


def downgrade() -> None:
    # ✅ REVERT ENUM BACK TO VARCHAR
    op.alter_column(
        'payments',
        'status',
        existing_type=sa.Enum('CREATED', 'SUCCESS', 'FAILED', name='paymentstatus'),
        type_=sa.VARCHAR(),
        nullable=True
    )

    op.alter_column(
        'payments',
        'currency',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.alter_column(
        'payments',
        'amount',
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True
    )

    op.drop_column('payments', 'updated_at')
    op.drop_column('payments', 'provider_signature')
    op.drop_column('payments', 'provider_payment_id')
    op.drop_column('payments', 'provider_order_id')
    op.drop_column('payments', 'provider')
