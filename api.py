from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Book
from app.database import get_session, init_db
from app.services import LibraryService
from openlibrary import fetch_book_from_api

app = FastAPI(
    title="Library Management API",
    description="A simple library management system API",
    version="1.0.0",
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BookCreate(BaseModel):
    isbn: str


class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str
    status: str = "available"


class MemberCreate(BaseModel):
    name: str


class MemberResponse(BaseModel):
    id: int
    name: str


class BorrowRequest(BaseModel):
    member_id: int
    isbn: str


class PaginatedBookResponse(BaseModel):
    """Paginated response for books."""
    items: List[BookResponse]
    total: int
    skip: int
    limit: int


class BorrowRecordResponse(BaseModel):
    """Response model for borrow records."""
    id: int
    member_id: int
    isbn: str
    borrow_date: str
    return_date: Optional[str] = None


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    return {"message": "Library Management API'ye hoş geldiniz!"}


@app.get("/books", response_model=PaginatedBookResponse)
async def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    title: Optional[str] = Query(None, description="Filter by title (partial match)"),
    status: Optional[str] = Query(None, description="Filter by status (available, borrowed)"),
    session: AsyncSession = Depends(get_session),
):
    """Tüm kitapları listeler (filtreleme ve sayfalama ile)"""
    service = LibraryService(session)
    books = await service.get_books(
        skip=skip, limit=limit, author=author, title=title, status=status
    )
    total = await service.count_books(author=author, title=title, status=status)

    return PaginatedBookResponse(
        items=[
            BookResponse(title=b.title, author=b.author, isbn=b.isbn, status=b.status)
            for b in books
        ],
        total=total,
        skip=skip,
        limit=limit,
    )


@app.post("/books", response_model=BookResponse)
async def add_book(
    book_create: BookCreate, session: AsyncSession = Depends(get_session)
):
    """ISBN ile yeni kitap ekler"""
    try:
        # API'den kitap bilgilerini al
        book_model: Book = await fetch_book_from_api(book_create.isbn)

        # Add book using service
        service = LibraryService(session)
        added_book = await service.add_book(book_model)

        return BookResponse(
            title=added_book.title,
            author=added_book.author,
            isbn=added_book.isbn,
            status=added_book.status,
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/books/{isbn}", response_model=BookResponse)
async def get_book(isbn: str, session: AsyncSession = Depends(get_session)):
    """ISBN ile belirli bir kitabı getirir"""
    service = LibraryService(session)
    book = await service.get_book(isbn)
    if book:
        return BookResponse(
            title=book.title, author=book.author, isbn=book.isbn, status=book.status
        )
    raise HTTPException(status_code=404, detail="Kitap bulunamadı")


@app.delete("/books/{isbn}")
async def delete_book(isbn: str, session: AsyncSession = Depends(get_session)):
    """ISBN ile kitabı siler"""
    service = LibraryService(session)
    result = await service.delete_book(isbn)
    if not result:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    return {"message": "Kitap silindi"}


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """API sağlık durumu"""
    service = LibraryService(session)
    books = await service.get_books(limit=1000)
    return {"status": "healthy", "books_count": len(books)}


# New endpoints for members and borrowing
@app.post("/members", response_model=MemberResponse)
async def create_member(
    member_create: MemberCreate, session: AsyncSession = Depends(get_session)
):
    """Yeni üye oluştur"""
    from app.repositories import MemberRepository

    repo = MemberRepository(session)
    member = await repo.create(member_create.name)
    return MemberResponse(id=member.id, name=member.name)


@app.get("/members/{member_id}", response_model=MemberResponse)
async def get_member(
    member_id: int, session: AsyncSession = Depends(get_session)
):
    """Belirli bir üyeyi getir"""
    from app.repositories import MemberRepository

    repo = MemberRepository(session)
    member = await repo.get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Üye bulunamadı")
    return MemberResponse(id=member.id, name=member.name)


@app.get("/members", response_model=List[MemberResponse])
async def get_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session),
):
    """Tüm üyeleri listele"""
    from app.repositories import MemberRepository

    repo = MemberRepository(session)
    members = await repo.get_all(skip=skip, limit=limit)
    return [MemberResponse(id=m.id, name=m.name) for m in members]


@app.post("/borrow")
async def borrow_book(
    borrow_request: BorrowRequest, session: AsyncSession = Depends(get_session)
):
    """Kitap ödünç al"""
    service = LibraryService(session)
    try:
        await service.borrow_book(borrow_request.member_id, borrow_request.isbn)
        return {"message": "Kitap başarıyla ödünç alındı"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/return")
async def return_book(
    borrow_request: BorrowRequest, session: AsyncSession = Depends(get_session)
):
    """Kitap iade et"""
    service = LibraryService(session)
    try:
        success = await service.return_book(borrow_request.member_id, borrow_request.isbn)
        if not success:
            raise HTTPException(status_code=404, detail="Ödünç kaydı bulunamadı")
        return {"message": "Kitap başarıyla iade edildi"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/members/{member_id}/borrows", response_model=List[BorrowRecordResponse])
async def get_member_borrows(
    member_id: int,
    active_only: bool = Query(False, description="Show only active borrows"),
    session: AsyncSession = Depends(get_session),
):
    """Üyenin ödünç alma geçmişini getir"""
    from app.repositories import BorrowRecordRepository, MemberRepository
    from datetime import datetime

    # Verify member exists
    member_repo = MemberRepository(session)
    member = await member_repo.get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Üye bulunamadı")

    # Get borrow records
    borrow_repo = BorrowRecordRepository(session)
    records = await borrow_repo.get_by_member_id(member_id, active_only=active_only)

    return [
        BorrowRecordResponse(
            id=r.id,
            member_id=r.member_id,
            isbn=r.isbn,
            borrow_date=r.borrow_date.isoformat() if r.borrow_date else "",
            return_date=r.return_date.isoformat() if r.return_date else None,
        )
        for r in records
    ]


@app.get("/books/{isbn}/borrows", response_model=List[BorrowRecordResponse])
async def get_book_borrows(
    isbn: str,
    active_only: bool = Query(False, description="Show only active borrows"),
    session: AsyncSession = Depends(get_session),
):
    """Kitabın ödünç alma geçmişini getir"""
    from app.repositories import BorrowRecordRepository, BookRepository

    # Verify book exists
    book_repo = BookRepository(session)
    book = await book_repo.get_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")

    # Get borrow records
    borrow_repo = BorrowRecordRepository(session)
    records = await borrow_repo.get_by_isbn(isbn, active_only=active_only)

    return [
        BorrowRecordResponse(
            id=r.id,
            member_id=r.member_id,
            isbn=r.isbn,
            borrow_date=r.borrow_date.isoformat() if r.borrow_date else "",
            return_date=r.return_date.isoformat() if r.return_date else None,
        )
        for r in records
    ]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
    )
