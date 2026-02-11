# Create debug script: debug_schema.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from sqlalchemy import inspect, text

# Create inspector
inspector = inspect(engine)

print("=== DATABASE STATE ===")
# Check payments table
if 'payments' in inspector.get_table_names():
    columns = inspector.get_columns('payments')
    print("Payments table columns:")
    for col in columns:
        print(f"  - {col['name']}: {col['type']}, nullable={col.get('nullable', True)}")
else:
    print("Payments table doesn't exist!")

print("\n=== MODEL STATE ===")
# Try to import Payment model
try:
    from app.models import Payment
    print("Payment model columns:")
    for column in Payment.__table__.columns:
        print(f"  - {column.name}: {column.type}, nullable={column.nullable}")
except ImportError as e:
    print(f"Cannot import Payment model: {e}")
except AttributeError as e:
    print(f"Payment model issue: {e}")

print("\n=== DIRECT SQL CHECK ===")
with engine.connect() as conn:
    # Check if payment_date exists
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'payments'
        ORDER BY ordinal_position
    """))
    
    for row in result:
        print(f"  - {row.column_name}: {row.data_type}, nullable={row.is_nullable}")