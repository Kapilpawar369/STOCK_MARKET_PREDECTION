# /home/tw/Stock_Pulse/alembic/versions/3c5eae763b4b_add_user_verification_fields.py

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql # Keep postgresql import

revision: str = '3c5eae763b4b'
down_revision: Union[str, Sequence[str], None] = '260266d03e39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands to ADD verification fields and REMOVE old tables (otp, orders) ###
    
    # 1. ADD is_verified with CRITICAL PostgreSQL FIX
    # The server_default is added here to assign 'false' to existing rows.
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), 
        nullable=False, 
        server_default=sa.text('false') 
    ))

    # 2. Add otp_code column (Nullable, fine as is)
    op.add_column('users', sa.Column('otp_code', sa.String(length=6), nullable=True))
    
    # 3. Add otp_expires_at column (Nullable, fine as is)
    op.add_column('users', sa.Column('otp_expires_at', sa.DateTime(timezone=True), nullable=True))
    
    # 4. CLEANUP: Remove the server_default so new insertions rely on SQLAlchemy/Model default.
    op.alter_column('users', 'is_verified', server_default=None, existing_type=sa.Boolean())
    
    # 5. FIX NULLABILITY ISSUE (If detected by autogenerate)
    # The autogenerate detected a change in 'users.is_deleted' from NULLABLE to NOT NULL.
    # We must explicitly set existing_server_default to avoid errors during upgrade/downgrade cycles.
    op.alter_column('users', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=True, # Based on the downgrade provided, it seems it was nullable=True before.
               existing_server_default=sa.text('false')) # Keep the default for existing rows
    
    # 6. REMOVE old tables/indexes (Detected by autogenerate)
    op.drop_index('ix_otp_id', table_name='otp', if_exists=True) # FIXED ERROR LINE
    op.drop_table('orders', if_exists=True) 
    op.drop_table('otp', if_exists=True)
    # ### end Alembic commands ###
    
def downgrade() -> None:
    """Downgrade schema."""
    # ### commands to REMOVE verification fields and RE-CREATE old tables (otp, orders) ###

    # 1. RE-CREATE old tables/indexes (Reversing the table drops)
    op.create_table('otp',
        sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('otp', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('expires_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column('is_used', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('otp_user_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('otp_pkey'))
    )
    op.create_index(op.f('ix_otp_id'), 'otp', ['id'], unique=False)
    
    op.create_table('orders',
        sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('symbol', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('price_per_unit', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
        sa.Column('total_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
        sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('status', postgresql.ENUM('PENDING', 'COMPLETED', 'CANCELLED', name='orderstatus'), autoincrement=False, nullable=False),
        sa.Column('payment_id', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], name=op.f('orders_payment_id_fkey')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('orders_user_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('orders_pkey'))
    )

    # 2. REMOVE verification fields (Reversing the column additions)
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'otp_code')
    op.drop_column('users', 'otp_expires_at')
    
    # 3. FIX NULLABILITY ISSUE (Reversing the change made in upgrade if needed)
    # This reverses the nullability change detected by autogenerate if it was unintended.
    op.alter_column('users', 'is_deleted',
               existing_type=sa.BOOLEAN(),
               nullable=False, # Reversing the nullable change
               existing_server_default=sa.text('false'))
    
    # ### end Alembic commands ###