from typing import List
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, ValidationError
import json
import os

from app.models import Book


class EBook(Book):
    """An E-Book that inherits from the unified Book model."""

    file_format: str

    def display_info(self) -> str:
        return f"{super().display_info()} [Format: {self.file_format}]"


class AudioBook(Book):
    """An Audio Book that inherits from the unified Book model."""

    duration: int

    def display_info(self) -> str:
        return f"{super().display_info()} [Duration: {self.duration} minutes]"


class Library:
    """Manages a collection of books using composition."""

    def __init__(self, name: str, json_path: str = "library.json"):
        self.name = name
        self._books: List[Book] = []
        self.json_path = json_path
        self.load_from_json(self.json_path)

    def add_book(self, book: Book) -> bool:
        """Add a Book domain object to the library."""
        if any(existing.isbn == book.isbn for existing in self._books):
            print("Bu ISBN kütüphanede zaten kayıtlı.")
            return False

        self._books.append(book)
        self.save_to_json(self.json_path)
        print(f"Kitap eklendi: {book.title} ({book.author})")
        return True

    def delete_book(self, isbn: str) -> bool:
        """Deleting books by ISBN number"""
        for book in self._books:
            if book.isbn == isbn:
                self._books.remove(book)
                self.save_to_json(self.json_path)  # Save changes
                return True
        return False
    
    def list_books(self) -> List[str]:
        """Return a list of human-readable book descriptions."""
        return [book.display_info() for book in self._books]

    def get_books(self) -> List[Book]:
        """Return all books as domain models."""
        return list(self._books)

    def find_book(self, title: str | None = None, isbn: str | None = None) -> Book | None:
        """Find a book by title or ISBN."""
        for book in self._books:
            if title and book.title.lower() == title.lower():
                return book
            if isbn and book.isbn == isbn:
                return book
        return None

    def save_to_json(self, filename: str):
        """Save books to JSON using model dicts."""
        with open(filename, "w", encoding="utf-8") as f:
            payload = []
            for book in self._books:
                data = book.model_dump()
                # Persist the concrete type so we can reconstruct EBook/AudioBook later
                data["type"] = book.__class__.__name__
                payload.append(data)

            json.dump(payload, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename: str):
        """Load books from JSON, instantiating the correct model type when possible."""
        if not os.path.exists(filename):
            return  # No file yet, nothing to load

        with open(filename, "r", encoding="utf-8") as f:
            books_data = json.load(f)

        self._books.clear()
        for data in books_data:
            book_type = data.get("type")
            if book_type == "EBook":
                book = EBook(**data)
            elif book_type == "AudioBook":
                book = AudioBook(**data)
            else:
                book = Book(**data)
            self._books.append(book)

    @property
    def total_books(self) -> int:
        return len(self._books)


@dataclass
class Member:
    """Represents a library member using dataclasses"""
    name: str
    member_id: int
    borrowed_books: List[Book] = field(default_factory=list)


class PydanticBook(BaseModel):
    """Book model with Pydantic validation"""
    title: str
    author: str
    isbn: str = Field(..., min_length=10, max_length=13)
    publication_year: int = Field(..., gt=1400)

