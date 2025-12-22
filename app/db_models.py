"""SQLModel database models for Book, Member, and BorrowRecord."""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class BookDB(SQLModel, table=True):
    """Database model for books."""

    __tablename__ = "books"

    isbn: str = Field(primary_key=True, max_length=13)
    title: str
    author: str
    status: str = Field(default="available")  # available, borrowed
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to borrow records
    borrow_records: list["BorrowRecordDB"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})


class MemberDB(SQLModel, table=True):
    """Database model for library members."""

    __tablename__ = "members"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    join_date: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to borrow records
    borrow_records: list["BorrowRecordDB"] = Relationship(back_populates="member", sa_relationship_kwargs={"lazy": "selectin"})


class BorrowRecordDB(SQLModel, table=True):
    """Database model for book borrowing records."""

    __tablename__ = "borrow_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="members.id")
    isbn: str = Field(foreign_key="books.isbn")
    borrow_date: datetime = Field(default_factory=datetime.utcnow)
    return_date: Optional[datetime] = None

    # Relationships
    member: MemberDB = Relationship(back_populates="borrow_records")
    book: BookDB = Relationship(back_populates="borrow_records")

