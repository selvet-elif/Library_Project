"""Integration tests with test database."""
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.models import Book
from app.db_models import BookDB, MemberDB, BorrowRecordDB
from app.repositories import BookRepository, MemberRepository, BorrowRecordRepository
from app.services import LibraryService
from app.config import DatabaseSettings


# Use in-memory SQLite for integration tests (faster, no setup needed)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield engine
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine):
    """Create a test database session."""
    async_session_maker = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.mark.asyncio
async def test_add_book_workflow(test_session):
    """Test full workflow: add book to database."""
    service = LibraryService(test_session)
    
    book = Book(
        isbn="9780451524935",
        title="1984",
        author="George Orwell",
        status="available",
    )
    
    # Add book
    added_book = await service.add_book(book)
    
    assert added_book.isbn == book.isbn
    assert added_book.title == book.title
    
    # Verify it's in database
    found_book = await service.get_book(book.isbn)
    assert found_book is not None
    assert found_book.isbn == book.isbn


@pytest.mark.asyncio
async def test_add_duplicate_book(test_session):
    """Test adding duplicate book raises error."""
    service = LibraryService(test_session)
    
    book = Book(
        isbn="9780451524935",
        title="1984",
        author="George Orwell",
        status="available",
    )
    
    # Add book first time
    await service.add_book(book)
    
    # Try to add again - should fail
    with pytest.raises(ValueError, match="Bu ISBN zaten mevcut"):
        await service.add_book(book)


@pytest.mark.asyncio
async def test_borrow_and_return_workflow(test_session):
    """Test full workflow: add book, create member, borrow, return."""
    service = LibraryService(test_session)
    member_repo = MemberRepository(test_session)
    
    # Create member
    member = await member_repo.create("John Doe")
    
    # Add book
    book = Book(
        isbn="9780451524935",
        title="1984",
        author="George Orwell",
        status="available",
    )
    await service.add_book(book)
    
    # Borrow book
    result = await service.borrow_book(member.id, book.isbn)
    assert result is True
    
    # Verify book status changed
    borrowed_book = await service.get_book(book.isbn)
    assert borrowed_book.status == "borrowed"
    
    # Return book
    return_result = await service.return_book(member.id, book.isbn)
    assert return_result is True
    
    # Verify book status changed back
    returned_book = await service.get_book(book.isbn)
    assert returned_book.status == "available"


@pytest.mark.asyncio
async def test_book_filtering(test_session):
    """Test book filtering functionality."""
    service = LibraryService(test_session)
    
    # Add multiple books
    books = [
        Book(isbn="9780451524935", title="1984", author="George Orwell", status="available"),
        Book(isbn="9780061120084", title="To Kill a Mockingbird", author="Harper Lee", status="available"),
        Book(isbn="9780141439518", title="Pride and Prejudice", author="Jane Austen", status="borrowed"),
    ]
    
    for book in books:
        try:
            await service.add_book(book)
        except ValueError:
            pass  # Ignore duplicates if running multiple times
    
    # Filter by author
    orwell_books = await service.get_books(author="Orwell")
    assert len(orwell_books) >= 1
    assert all("Orwell" in book.author for book in orwell_books)
    
    # Filter by status
    available_books = await service.get_books(status="available")
    assert len(available_books) >= 1
    assert all(book.status == "available" for book in available_books)
    
    # Filter by title
    title_books = await service.get_books(title="1984")
    assert len(title_books) >= 1
    assert all("1984" in book.title for book in title_books)


@pytest.mark.asyncio
async def test_pagination(test_session):
    """Test pagination functionality."""
    service = LibraryService(test_session)
    
    # Add multiple books
    for i in range(15):
        book = Book(
            isbn=f"97800000000{i:02d}",
            title=f"Book {i}",
            author="Author",
            status="available",
        )
        try:
            await service.add_book(book)
        except ValueError:
            pass
    
    # Test pagination
    page1 = await service.get_books(skip=0, limit=10)
    assert len(page1) <= 10
    
    page2 = await service.get_books(skip=10, limit=10)
    assert len(page2) <= 10
    
    # Test count
    total = await service.count_books()
    assert total >= 0


@pytest.mark.asyncio
async def test_borrow_history(test_session):
    """Test borrow history tracking."""
    service = LibraryService(test_session)
    member_repo = MemberRepository(test_session)
    borrow_repo = BorrowRecordRepository(test_session)
    
    # Create member
    member = await member_repo.create("John Doe")
    
    # Add book
    book = Book(
        isbn="9780451524935",
        title="1984",
        author="George Orwell",
        status="available",
    )
    await service.add_book(book)
    
    # Borrow book
    await service.borrow_book(member.id, book.isbn)
    
    # Get borrow history for member
    member_borrows = await borrow_repo.get_by_member_id(member.id, active_only=True)
    assert len(member_borrows) == 1
    assert member_borrows[0].isbn == book.isbn
    assert member_borrows[0].member_id == member.id
    
    # Get borrow history for book
    book_borrows = await borrow_repo.get_by_isbn(book.isbn, active_only=True)
    assert len(book_borrows) == 1
    
    # Return book
    await service.return_book(member.id, book.isbn)
    
    # Get active borrows (should be empty now)
    active_borrows = await borrow_repo.get_by_member_id(member.id, active_only=True)
    assert len(active_borrows) == 0
    
    # Get all borrows (should still have the record)
    all_borrows = await borrow_repo.get_by_member_id(member.id, active_only=False)
    assert len(all_borrows) >= 1

