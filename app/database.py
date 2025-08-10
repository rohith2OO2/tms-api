from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import get_settings

# Load settings
settings = get_settings()

# Create the asynchronous engine
engine = create_async_engine(
    settings.DATABASE_URL,  # Example: postgresql+asyncpg://user:pass@tms_db:5432/dbname
    echo=False,              # Change to True for SQL debug logging
    future=True,
)

# Create async session factory
async_session_factory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Base class for declarative models
Base = declarative_base()

# Main dependency for FastAPI routes
async def get_db():
    """Yield an async DB session (used in FastAPI Depends)."""
    async with async_session_factory() as session:
        yield session

# Alias for backward compatibility in older code
# This helps avoid changing existing imports like:
# from database import get_session
get_session = get_db
