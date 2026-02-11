# Edit: alembic/versions/6e449f3834d8_add_payment_date_to_payments.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql  # if using PostgreSQL

def upgrade() -> None:
    """Upgrade schema."""
    # Add the missing payment_date column
    op.add_column('payments', sa.Column('payment_date', sa.Date(), nullable=True))
    
    # Optional: Update existing rows with a default date
    op.execute("UPDATE payments SET payment_date = CURRENT_DATE WHERE payment_date IS NULL")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('payments', 'payment_date')
