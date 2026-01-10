"""Tests for service layer."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services import LibraryService
from app.models import Book
from app.db_models import BookDB, MemberDB, BorrowRecordDB


class TestLibraryService:
    """Tests for LibraryService."""

    @pytest.mark.asyncio
    async def test_add_book_success(self, mock_async_session, sample_book):
        """Test adding a new book successfully."""
        service = LibraryService(mock_async_session)
        
        # Mock repository methods
        service.book_repo.get_by_isbn = AsyncMock(return_value=None)
        mock_db_book = BookDB(
            isbn=sample_book.isbn,
            title=sample_book.title,
            author=sample_book.author,
            status=sample_book.status,
        )
        service.book_repo.create = AsyncMock(return_value=mock_db_book)
        service.book_repo.to_domain = MagicMock(return_value=sample_book)

        result = await service.add_book(sample_book)

        assert result.isbn == sample_book.isbn
        service.book_repo.get_by_isbn.assert_called_once_with(sample_book.isbn)
        service.book_repo.create.assert_called_once_with(sample_book)

    @pytest.mark.asyncio
    async def test_add_book_duplicate(self, mock_async_session, sample_book, sample_book_db):
        """Test adding a duplicate book raises error."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_by_isbn = AsyncMock(return_value=sample_book_db)

        with pytest.raises(ValueError, match="Bu ISBN zaten mevcut"):
            await service.add_book(sample_book)

    @pytest.mark.asyncio
    async def test_get_book_found(self, mock_async_session, sample_book, sample_book_db):
        """Test getting a book that exists."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_by_isbn = AsyncMock(return_value=sample_book_db)
        service.book_repo.to_domain = MagicMock(return_value=sample_book)

        result = await service.get_book(sample_book.isbn)

        assert result == sample_book
        assert result.isbn == sample_book.isbn

    @pytest.mark.asyncio
    async def test_get_book_not_found(self, mock_async_session):
        """Test getting a book that doesn't exist."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_by_isbn = AsyncMock(return_value=None)

        result = await service.get_book("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_books_no_filters(self, mock_async_session, sample_book_db):
        """Test getting books without filters."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_all = AsyncMock(return_value=[sample_book_db])
        service.book_repo.to_domain = MagicMock(return_value=Book(
            isbn=sample_book_db.isbn,
            title=sample_book_db.title,
            author=sample_book_db.author,
            status=sample_book_db.status,
        ))

        books = await service.get_books(skip=0, limit=10)

        assert len(books) == 1
        service.book_repo.get_all.assert_called_once_with(
            skip=0, limit=10, author=None, title=None, status=None
        )

    @pytest.mark.asyncio
    async def test_get_books_with_filters(self, mock_async_session):
        """Test getting books with filters."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_all = AsyncMock(return_value=[])
        service.book_repo.to_domain = MagicMock()

        books = await service.get_books(
            skip=0, limit=10, author="Orwell", title="1984", status="available"
        )

        assert len(books) == 0
        service.book_repo.get_all.assert_called_once_with(
            skip=0, limit=10, author="Orwell", title="1984", status="available"
        )

    @pytest.mark.asyncio
    async def test_count_books(self, mock_async_session):
        """Test counting books."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.count = AsyncMock(return_value=5)

        count = await service.count_books(author="Orwell")

        assert count == 5
        service.book_repo.count.assert_called_once_with(author="Orwell", title=None, status=None)

    @pytest.mark.asyncio
    async def test_delete_book(self, mock_async_session):
        """Test deleting a book."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.delete = AsyncMock(return_value=True)

        result = await service.delete_book("9780451524935")

        assert result is True
        service.book_repo.delete.assert_called_once_with("9780451524935")

    @pytest.mark.asyncio
    async def test_borrow_book_success(self, mock_async_session, sample_book_db):
        """Test borrowing a book successfully."""
        service = LibraryService(mock_async_session)
        
        available_book = BookDB(
            isbn="9780451524935",
            title="1984",
            author="George Orwell",
            status="available",
        )
        service.book_repo.get_by_isbn = AsyncMock(return_value=available_book)
        service.borrow_repo.get_active_by_isbn = AsyncMock(return_value=None)
        service.borrow_repo.create = AsyncMock()
        service.book_repo.update_status = AsyncMock(return_value=True)

        result = await service.borrow_book(1, "9780451524935")

        assert result is True
        service.borrow_repo.create.assert_called_once_with(1, "9780451524935")
        service.book_repo.update_status.assert_called_once_with("9780451524935", "borrowed")

    @pytest.mark.asyncio
    async def test_borrow_book_not_found(self, mock_async_session):
        """Test borrowing a book that doesn't exist."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_by_isbn = AsyncMock(return_value=None)

        with pytest.raises(ValueError, match="Kitap bulunamadı"):
            await service.borrow_book(1, "nonexistent")

    @pytest.mark.asyncio
    async def test_borrow_book_already_borrowed_status(self, mock_async_session):
        """Test borrowing a book that's already borrowed (by status)."""
        service = LibraryService(mock_async_session)
        
        borrowed_book = BookDB(
            isbn="9780451524935",
            title="1984",
            author="George Orwell",
            status="borrowed",
        )
        service.book_repo.get_by_isbn = AsyncMock(return_value=borrowed_book)

        with pytest.raises(ValueError, match="Kitap şu anda ödünç alınamaz"):
            await service.borrow_book(1, "9780451524935")

    @pytest.mark.asyncio
    async def test_borrow_book_already_borrowed_record(self, mock_async_session, sample_book_db, sample_borrow_record_db):
        """Test borrowing a book that has an active borrow record."""
        service = LibraryService(mock_async_session)
        
        sample_book_db.status = "available"
        service.book_repo.get_by_isbn = AsyncMock(return_value=sample_book_db)
        service.borrow_repo.get_active_by_isbn = AsyncMock(return_value=sample_borrow_record_db)

        with pytest.raises(ValueError, match="Kitap zaten ödünç alınmış"):
            await service.borrow_book(1, "9780451524935")

    @pytest.mark.asyncio
    async def test_return_book_success(self, mock_async_session, sample_book_db):
        """Test returning a book successfully."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_by_isbn = AsyncMock(return_value=sample_book_db)
        service.borrow_repo.return_book = AsyncMock(return_value=True)
        service.book_repo.update_status = AsyncMock(return_value=True)

        result = await service.return_book(1, "9780451524935")

        assert result is True
        service.borrow_repo.return_book.assert_called_once_with(1, "9780451524935")
        service.book_repo.update_status.assert_called_once_with("9780451524935", "available")

    @pytest.mark.asyncio
    async def test_return_book_not_found(self, mock_async_session):
        """Test returning a book that doesn't exist."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_by_isbn = AsyncMock(return_value=None)

        with pytest.raises(ValueError, match="Kitap bulunamadı"):
            await service.return_book(1, "nonexistent")

    @pytest.mark.asyncio
    async def test_return_book_no_record(self, mock_async_session, sample_book_db):
        """Test returning a book when no borrow record exists."""
        service = LibraryService(mock_async_session)
        
        service.book_repo.get_by_isbn = AsyncMock(return_value=sample_book_db)
        service.borrow_repo.return_book = AsyncMock(return_value=False)
        service.book_repo.update_status = AsyncMock()

        result = await service.return_book(1, "9780451524935")

        assert result is False
        # Should not update status if return failed
        service.book_repo.update_status.assert_not_called()

