"""Database connection and session management using SQLModel."""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db_models import BookDB, MemberDB, BorrowRecordDB  # Import to register models

# Async engine for SQLModel
async_engine = create_async_engine(
    settings.database_url,
    echo=True,  # Log SQL queries
    future=True,
)

# Sync engine for migrations (Alembic)
sync_engine = create_engine(
    settings.sync_database_url,
    echo=True,
)

# Async session factory
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """Dependency for FastAPI to get async database session."""
    async with async_session_maker() as session:
        yield session


def init_db():
    """Initialize database tables (call this on startup)."""
    SQLModel.metadata.create_all(sync_engine)

