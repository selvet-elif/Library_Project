"""Pytest configuration and shared fixtures."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models import Book
from app.db_models import BookDB, MemberDB, BorrowRecordDB


@pytest.fixture
def sample_book():
    """Create a sample Book domain model."""
    return Book(
        isbn="9780451524935",
        title="1984",
        author="George Orwell",
        status="available",
    )


@pytest.fixture
def sample_book_db():
    """Create a sample BookDB model."""
    return BookDB(
        isbn="9780451524935",
        title="1984",
        author="George Orwell",
        status="available",
        created_at=datetime.utcnow(),
    )


@pytest.fixture
def sample_member_db():
    """Create a sample MemberDB model."""
    return MemberDB(
        id=1,
        name="John Doe",
        join_date=datetime.utcnow(),
    )


@pytest.fixture
def sample_borrow_record_db():
    """Create a sample BorrowRecordDB model."""
    return BorrowRecordDB(
        id=1,
        member_id=1,
        isbn="9780451524935",
        borrow_date=datetime.utcnow(),
        return_date=None,
    )


@pytest.fixture
def mock_async_session():
    """Create a mock AsyncSession for repository tests."""
    session = AsyncMock(spec=AsyncSession)
    
    # Mock common session methods
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    
    return session


@pytest.fixture
def mock_result():
    """Create a mock result object for SQLAlchemy queries."""
    result = MagicMock()
    result.scalar_one_or_none = MagicMock()
    result.scalar_one = MagicMock(return_value=0)
    result.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))
    result.rowcount = 1
    return result

