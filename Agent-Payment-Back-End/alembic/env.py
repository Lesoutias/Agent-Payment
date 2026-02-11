import os
import sys
from logging.config import fileConfig

from app.models import Payment, Agent, User  # Ensure models are imported so their metadata is registered

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.database import Base  # or from app.models import Base
target_metadata = Base.metadata

# Add your app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your SQLAlchemy Base
from app.database import Base  # Adjust based on your actual structure
# OR if you have models directly
# from app.models import Base

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set target_metadata
target_metadata = Base.metadata

def run_migrations_offline():
    # ... existing code ...
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    # ... rest of offline function

def run_migrations_online():
    # ... existing code ...
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        # ... rest of online function