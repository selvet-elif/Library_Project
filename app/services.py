"""Service layer for business logic using repositories."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Book
from app.repositories import (
    BookRepository,
    MemberRepository,
    BorrowRecordRepository,
)


class LibraryService:
    """Service for library operations using database repositories."""

    def __init__(self, session: AsyncSession):
        self.book_repo = BookRepository(session)
        self.member_repo = MemberRepository(session)
        self.borrow_repo = BorrowRecordRepository(session)

    async def add_book(self, book: Book) -> Book:
        """Add a book to the library."""
        # Check if book already exists
        existing = await self.book_repo.get_by_isbn(book.isbn)
        if existing:
            raise ValueError("Bu ISBN zaten mevcut")

        # Create book in database
        db_book = await self.book_repo.create(book)
        return self.book_repo.to_domain(db_book)

    async def get_book(self, isbn: str) -> Optional[Book]:
        """Get a book by ISBN."""
        db_book = await self.book_repo.get_by_isbn(isbn)
        if db_book:
            return self.book_repo.to_domain(db_book)
        return None

    async def get_books(
        self,
        skip: int = 0,
        limit: int = 100,
        author: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Book]:
        """Get all books with pagination and filtering."""
        db_books = await self.book_repo.get_all(
            skip=skip, limit=limit, author=author, title=title, status=status
        )
        return [self.book_repo.to_domain(db_book) for db_book in db_books]

    async def count_books(
        self,
        author: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
    ) -> int:
        """Count books matching filters."""
        return await self.book_repo.count(author=author, title=title, status=status)

    async def delete_book(self, isbn: str) -> bool:
        """Delete a book by ISBN."""
        return await self.book_repo.delete(isbn)

    async def borrow_book(self, member_id: int, isbn: str) -> bool:
        """Borrow a book for a member."""
        # Check if book exists and is available
        db_book = await self.book_repo.get_by_isbn(isbn)
        if not db_book:
            raise ValueError("Kitap bulunamadı")

        if db_book.status != "available":
            raise ValueError("Kitap şu anda ödünç alınamaz")

        # Check if already borrowed
        existing_record = await self.borrow_repo.get_active_by_isbn(isbn)
        if existing_record:
            raise ValueError("Kitap zaten ödünç alınmış")

        # Create borrow record and update book status
        await self.borrow_repo.create(member_id, isbn)
        await self.book_repo.update_status(isbn, "borrowed")
        return True

    async def return_book(self, member_id: int, isbn: str) -> bool:
        """Return a borrowed book."""
        # Check if book exists
        db_book = await self.book_repo.get_by_isbn(isbn)
        if not db_book:
            raise ValueError("Kitap bulunamadı")

        # Mark as returned
        success = await self.borrow_repo.return_book(member_id, isbn)
        if success:
            await self.book_repo.update_status(isbn, "available")
        return success

