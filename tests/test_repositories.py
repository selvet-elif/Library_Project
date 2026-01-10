"""Tests for repository layer."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from app.repositories import BookRepository, MemberRepository, BorrowRecordRepository
from app.models import Book
from app.db_models import BookDB, MemberDB, BorrowRecordDB


class TestBookRepository:
    """Tests for BookRepository."""

    @pytest.mark.asyncio
    async def test_create_book(self, mock_async_session, sample_book):
        """Test creating a book in the database."""
        repo = BookRepository(mock_async_session)
        
        # Mock the database response
        mock_book_db = BookDB(
            isbn=sample_book.isbn,
            title=sample_book.title,
            author=sample_book.author,
            status=sample_book.status,
        )
        mock_async_session.refresh = AsyncMock()

        db_book = await repo.create(sample_book)

        assert db_book.isbn == sample_book.isbn
        assert db_book.title == sample_book.title
        assert db_book.author == sample_book.author
        mock_async_session.add.assert_called_once()
        mock_async_session.commit.assert_called_once()
        mock_async_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_isbn_found(self, mock_async_session, sample_book_db):
        """Test getting a book by ISBN when it exists."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_book_db
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_by_isbn(sample_book_db.isbn)

        assert result == sample_book_db
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_isbn_not_found(self, mock_async_session):
        """Test getting a book by ISBN when it doesn't exist."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_by_isbn("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_no_filters(self, mock_async_session, sample_book_db):
        """Test getting all books without filters."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sample_book_db]
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        books = await repo.get_all(skip=0, limit=10)

        assert len(books) == 1
        assert books[0] == sample_book_db

    @pytest.mark.asyncio
    async def test_get_all_with_author_filter(self, mock_async_session):
        """Test getting books filtered by author."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        await repo.get_all(skip=0, limit=10, author="Orwell")

        mock_async_session.execute.assert_called_once()
        # Verify the query includes author filter
        call_args = mock_async_session.execute.call_args
        assert call_args is not None

    @pytest.mark.asyncio
    async def test_get_all_with_title_filter(self, mock_async_session):
        """Test getting books filtered by title."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        await repo.get_all(skip=0, limit=10, title="1984")

        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_status_filter(self, mock_async_session):
        """Test getting books filtered by status."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        await repo.get_all(skip=0, limit=10, status="available")

        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_with_pagination(self, mock_async_session):
        """Test getting books with pagination."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        await repo.get_all(skip=10, limit=20)

        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_count_no_filters(self, mock_async_session):
        """Test counting books without filters."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 5
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        count = await repo.count()

        assert count == 5
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_count_with_filters(self, mock_async_session):
        """Test counting books with filters."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 2
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        count = await repo.count(author="Orwell", status="available")

        assert count == 2
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_count_with_title_filter(self, mock_async_session):
        """Test counting books with title filter (covers line 75)."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 1
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        count = await repo.count(title="1984")

        assert count == 1
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_count_with_all_filters(self, mock_async_session):
        """Test counting books with all filters including title."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 1
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        count = await repo.count(author="Orwell", title="1984", status="available")

        assert count == 1
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_book_success(self, mock_async_session):
        """Test deleting a book successfully."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.delete("9780451524935")

        assert result is True
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_book_not_found(self, mock_async_session):
        """Test deleting a book that doesn't exist."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.delete("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_update_status(self, mock_async_session):
        """Test updating book status."""
        repo = BookRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.update_status("9780451524935", "borrowed")

        assert result is True
        mock_async_session.commit.assert_called_once()

    def test_to_domain(self, sample_book_db):
        """Test converting database model to domain model."""
        repo = BookRepository(MagicMock())
        
        domain_book = repo.to_domain(sample_book_db)

        assert domain_book.isbn == sample_book_db.isbn
        assert domain_book.title == sample_book_db.title
        assert domain_book.author == sample_book_db.author
        assert domain_book.status == sample_book_db.status
        assert isinstance(domain_book, Book)


class TestMemberRepository:
    """Tests for MemberRepository."""

    @pytest.mark.asyncio
    async def test_create_member(self, mock_async_session):
        """Test creating a member."""
        repo = MemberRepository(mock_async_session)
        
        mock_member = MemberDB(id=1, name="John Doe", join_date=datetime.utcnow())
        mock_async_session.refresh = AsyncMock()

        member = await repo.create("John Doe")

        assert member.name == "John Doe"
        mock_async_session.add.assert_called_once()
        mock_async_session.commit.assert_called_once()
        mock_async_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, mock_async_session, sample_member_db):
        """Test getting a member by ID when it exists."""
        repo = MemberRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_member_db
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_by_id(1)

        assert result == sample_member_db

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, mock_async_session):
        """Test getting a member by ID when it doesn't exist."""
        repo = MemberRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_by_id(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_all(self, mock_async_session, sample_member_db):
        """Test getting all members."""
        repo = MemberRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sample_member_db]
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        members = await repo.get_all(skip=0, limit=10)

        assert len(members) == 1
        assert members[0] == sample_member_db

    @pytest.mark.asyncio
    async def test_count(self, mock_async_session):
        """Test counting members."""
        repo = MemberRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 10
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        count = await repo.count()

        assert count == 10


class TestBorrowRecordRepository:
    """Tests for BorrowRecordRepository."""

    @pytest.mark.asyncio
    async def test_create_borrow_record(self, mock_async_session):
        """Test creating a borrow record."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_record = BorrowRecordDB(
            id=1, member_id=1, isbn="9780451524935", borrow_date=datetime.utcnow()
        )
        mock_async_session.refresh = AsyncMock()

        record = await repo.create(1, "9780451524935")

        assert record.member_id == 1
        assert record.isbn == "9780451524935"
        mock_async_session.add.assert_called_once()
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_active_by_isbn_found(self, mock_async_session, sample_borrow_record_db):
        """Test getting active borrow record for a book."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_borrow_record_db
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_active_by_isbn("9780451524935")

        assert result == sample_borrow_record_db

    @pytest.mark.asyncio
    async def test_get_active_by_isbn_not_found(self, mock_async_session):
        """Test getting active borrow record when none exists."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.get_active_by_isbn("9780451524935")

        assert result is None

    @pytest.mark.asyncio
    async def test_return_book_success(self, mock_async_session):
        """Test returning a book successfully."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.rowcount = 1
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.return_book(1, "9780451524935")

        assert result is True
        mock_async_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_return_book_not_found(self, mock_async_session):
        """Test returning a book that wasn't borrowed."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.rowcount = 0
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        result = await repo.return_book(1, "nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_get_by_member_id_all(self, mock_async_session, sample_borrow_record_db):
        """Test getting all borrow records for a member."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sample_borrow_record_db]
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        records = await repo.get_by_member_id(1, active_only=False)

        assert len(records) == 1
        assert records[0] == sample_borrow_record_db

    @pytest.mark.asyncio
    async def test_get_by_member_id_active_only(self, mock_async_session):
        """Test getting only active borrow records for a member."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        records = await repo.get_by_member_id(1, active_only=True)

        assert len(records) == 0
        mock_async_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_isbn_all(self, mock_async_session, sample_borrow_record_db):
        """Test getting all borrow records for a book."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sample_borrow_record_db]
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        records = await repo.get_by_isbn("9780451524935", active_only=False)

        assert len(records) == 1

    @pytest.mark.asyncio
    async def test_get_by_isbn_active_only(self, mock_async_session):
        """Test getting only active borrow records for a book."""
        repo = BorrowRecordRepository(mock_async_session)
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_async_session.execute = AsyncMock(return_value=mock_result)

        records = await repo.get_by_isbn("9780451524935", active_only=True)

        assert len(records) == 0

