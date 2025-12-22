"""Repository classes for database operations."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlmodel import SQLModel

from app.models import Book
from app.db_models import BookDB, MemberDB, BorrowRecordDB


class BookRepository:
    """Repository for book database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, book: Book) -> BookDB:
        """Create a new book in the database."""
        db_book = BookDB(
            isbn=book.isbn,
            title=book.title,
            author=book.author,
            status=book.status,
        )
        self.session.add(db_book)
        await self.session.commit()
        await self.session.refresh(db_book)
        return db_book

    async def get_by_isbn(self, isbn: str) -> Optional[BookDB]:
        """Get a book by ISBN."""
        result = await self.session.execute(select(BookDB).where(BookDB.isbn == isbn))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        author: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[BookDB]:
        """Get all books with pagination and filtering."""
        query = select(BookDB)

        # Apply filters
        if author:
            query = query.where(BookDB.author.ilike(f"%{author}%"))
        if title:
            query = query.where(BookDB.title.ilike(f"%{title}%"))
        if status:
            query = query.where(BookDB.status == status)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def count(
        self,
        author: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
    ) -> int:
        """Count books matching filters."""
        from sqlalchemy import func

        query = select(func.count(BookDB.isbn))

        # Apply same filters as get_all
        if author:
            query = query.where(BookDB.author.ilike(f"%{author}%"))
        if title:
            query = query.where(BookDB.title.ilike(f"%{title}%"))
        if status:
            query = query.where(BookDB.status == status)

        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete(self, isbn: str) -> bool:
        """Delete a book by ISBN."""
        result = await self.session.execute(
            delete(BookDB).where(BookDB.isbn == isbn)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def update_status(self, isbn: str, status: str) -> bool:
        """Update book status."""
        result = await self.session.execute(
            update(BookDB).where(BookDB.isbn == isbn).values(status=status)
        )
        await self.session.commit()
        return result.rowcount > 0

    def to_domain(self, db_book: BookDB) -> Book:
        """Convert database model to domain model."""
        return Book(
            isbn=db_book.isbn,
            title=db_book.title,
            author=db_book.author,
            status=db_book.status,
        )


class MemberRepository:
    """Repository for member database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str) -> MemberDB:
        """Create a new member."""
        member = MemberDB(name=name)
        self.session.add(member)
        await self.session.commit()
        await self.session.refresh(member)
        return member

    async def get_by_id(self, member_id: int) -> Optional[MemberDB]:
        """Get a member by ID."""
        result = await self.session.execute(
            select(MemberDB).where(MemberDB.id == member_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[MemberDB]:
        """Get all members with pagination."""
        result = await self.session.execute(
            select(MemberDB).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        """Count total members."""
        from sqlalchemy import func

        result = await self.session.execute(select(func.count(MemberDB.id)))
        return result.scalar_one()


class BorrowRecordRepository:
    """Repository for borrow record database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, member_id: int, isbn: str) -> BorrowRecordDB:
        """Create a borrow record."""
        record = BorrowRecordDB(member_id=member_id, isbn=isbn)
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def get_active_by_isbn(self, isbn: str) -> Optional[BorrowRecordDB]:
        """Get active borrow record for a book (not returned)."""
        result = await self.session.execute(
            select(BorrowRecordDB)
            .where(BorrowRecordDB.isbn == isbn)
            .where(BorrowRecordDB.return_date.is_(None))
        )
        return result.scalar_one_or_none()

    async def return_book(self, member_id: int, isbn: str) -> bool:
        """Mark a book as returned."""
        from datetime import datetime

        result = await self.session.execute(
            update(BorrowRecordDB)
            .where(BorrowRecordDB.member_id == member_id)
            .where(BorrowRecordDB.isbn == isbn)
            .where(BorrowRecordDB.return_date.is_(None))
            .values(return_date=datetime.utcnow())
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_by_member_id(
        self, member_id: int, active_only: bool = False
    ) -> List[BorrowRecordDB]:
        """Get borrow records for a member."""
        query = select(BorrowRecordDB).where(BorrowRecordDB.member_id == member_id)

        if active_only:
            query = query.where(BorrowRecordDB.return_date.is_(None))

        result = await self.session.execute(query.order_by(BorrowRecordDB.borrow_date.desc()))
        return list(result.scalars().all())

    async def get_by_isbn(
        self, isbn: str, active_only: bool = False
    ) -> List[BorrowRecordDB]:
        """Get borrow records for a book."""
        query = select(BorrowRecordDB).where(BorrowRecordDB.isbn == isbn)

        if active_only:
            query = query.where(BorrowRecordDB.return_date.is_(None))

        result = await self.session.execute(query.order_by(BorrowRecordDB.borrow_date.desc()))
        return list(result.scalars().all())

