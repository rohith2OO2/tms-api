from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from config import get_settings

settings = get_settings()

# Create the asynchronous engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,       # Set to True to enable SQL query logging
    future=True,
)

# Create async session factory
async_session_factory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Base class for models
Base = declarative_base()

# Dependency function to get async DB session in FastAPI
async def get_db():
    async with async_session_factory() as session:
        yield session
