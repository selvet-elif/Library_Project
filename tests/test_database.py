"""Tests for database connection and initialization."""
import pytest
from unittest.mock import patch, MagicMock

from app.database import get_session, init_db, async_session_maker, sync_engine
from app.db_models import BookDB, MemberDB, BorrowRecordDB


@pytest.mark.asyncio
async def test_get_session():
    """Test that get_session is an async generator."""
    session_gen = get_session()
    
    # Should be an async generator
    assert hasattr(session_gen, "__anext__")
    
    # Close the generator
    await session_gen.aclose()


def test_init_db():
    """Test database initialization."""
    # Mock SQLModel.metadata.create_all
    with patch("app.database.SQLModel") as mock_sqlmodel:
        mock_metadata = MagicMock()
        mock_sqlmodel.metadata = mock_metadata
        
        init_db()
        
        # Verify create_all was called with sync_engine
        mock_metadata.create_all.assert_called_once()


def test_async_session_maker_exists():
    """Test that async_session_maker is configured."""
    assert async_session_maker is not None


def test_sync_engine_exists():
    """Test that sync_engine is configured."""
    assert sync_engine is not None


class TestDatabaseModels:
    """Tests for database models."""

    def test_book_db_model(self):
        """Test BookDB model creation."""
        from datetime import datetime
        
        book = BookDB(
            isbn="9780451524935",
            title="1984",
            author="George Orwell",
            status="available",
            created_at=datetime.utcnow(),
        )
        
        assert book.isbn == "9780451524935"
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.status == "available"
        assert book.created_at is not None

    def test_member_db_model(self):
        """Test MemberDB model creation."""
        from datetime import datetime
        
        member = MemberDB(
            id=1,
            name="John Doe",
            join_date=datetime.utcnow(),
        )
        
        assert member.id == 1
        assert member.name == "John Doe"
        assert member.join_date is not None

    def test_borrow_record_db_model(self):
        """Test BorrowRecordDB model creation."""
        from datetime import datetime
        
        record = BorrowRecordDB(
            id=1,
            member_id=1,
            isbn="9780451524935",
            borrow_date=datetime.utcnow(),
            return_date=None,
        )
        
        assert record.id == 1
        assert record.member_id == 1
        assert record.isbn == "9780451524935"
        assert record.borrow_date is not None
        assert record.return_date is None

    def test_borrow_record_with_return_date(self):
        """Test BorrowRecordDB with return date."""
        from datetime import datetime
        
        return_date = datetime.utcnow()
        record = BorrowRecordDB(
            id=1,
            member_id=1,
            isbn="9780451524935",
            borrow_date=datetime.utcnow(),
            return_date=return_date,
        )
        
        assert record.return_date == return_date

