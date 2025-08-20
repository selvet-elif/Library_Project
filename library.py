from typing import List
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, ValidationError
import json
import os
from openlibrary import fetch_book_from_api

@dataclass
class Book:
    """Single book in the library"""
    title: str
    author: str
    isbn: str
    is_borrowed: bool = False

    """ Returns a readable string of the book."""
    def __str__(self):
        return (f"Title: {self.title}, "
                f"Author: {self.author}, "
                f"ISBN: {self.isbn}, "
                f"Borrowed: {'Yes' if self.is_borrowed else 'No'}")

    def borrow_book(self):
        """Mark the book as borrowed"""
        if not self.is_borrowed:
            self.is_borrowed = True
        else:
            raise ValueError(f"'{self.title}' is already borrowed.")

    def return_book(self):
        """Mark the book as returned"""
        if self.is_borrowed:
            self.is_borrowed = False  
        else:
            raise ValueError(f"'{self.title}' was not borrowed.")

    def display_info(self) -> str:
        """Display the book name and its author"""
        return f"'{self.title}' by {self.author}"

    def to_dict(self):   # Function to save the changes to JSON file.
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "is_borrowed": self.is_borrowed
        }


class EBook(Book):
    """An E-Book that inherits from Book"""
    def __init__(self, title: str, author: str, isbn: str, file_format: str):
        super().__init__(title, author, isbn)
        self.file_format = file_format

    def to_dict(self):   # Function to save the changes to JSON file.
        data = super().to_dict()
        data["file_format"] = self.file_format
        return data

    def display_info(self) -> str:
        return f"{super().display_info()} [Format: {self.file_format}]"


class AudioBook(Book):
    """An Audio Book that inherits from Book"""
    def __init__(self, title: str, author: str, isbn: str, duration_in_minutes: int):
        super().__init__(title, author, isbn)
        self.duration = duration_in_minutes
        
    def to_dict(self):   # Function to save the changes to JSON file.
        data = super().to_dict()
        data["duration"] = self.duration
        return data

    def display_info(self) -> str:
        return f"{super().display_info()} [Duration: {self.duration} minutes]"


class Library:
    """Manages a collection of books using composition"""
    def __init__(self, name: str, json_path: str = "library.json"):
        self.name = name
        self._books = []
        self.json_path = json_path
        self.load_from_json(self.json_path)
    
    
    def add_book(self, isbn: str) -> bool:
        
        """Add a book by fetching details from OpenLibrary API"""
        data = fetch_book_from_api(isbn)
        if not data:
            print("Kitap bilgisi alınamadı, eklenemedi.")
            return False
        # To get title of the book
        title = data.get("title", "Unknown Title")
        # To get Author's names
        authors = data.get("authors", [])
        if authors and isinstance(authors[0], dict):
            author = " & ".join(a.get("name", "Unknown") for a in authors)
        elif authors and isinstance(authors[0], str):
            author = " & ".join(authors)
        else:
            author = "Unknown Author"

        # If the book is already in the library, doen't add.
        if any(book.isbn == isbn for book in self._books):
            print("Bu ISBN kütüphanede zaten kayıtlı.")
            return False

        new_book = Book(title=title, author=author, isbn=isbn)
        self._books.append(new_book)
        self.save_to_json(self.json_path)
        print(f"Kitap eklendi: {title} ({author})")
        return True

    def delete_book(self, isbn: str) -> bool:
        """Deleting books by ISBN number"""
        for book in self._books:
            if book.isbn == isbn:
                self._books.remove(book)
                self.save_to_json(self.json_path)  # Save changes
                return True
        return False
    
    def list_books(self):
        return [book.display_info() for book in self._books]

    """Finds a book by its title or its ISBN number."""
    def find_book(self, title: str = None, isbn: str = None) -> Book | None:
        for book in self._books:
            if (book and book.title.lower() == title.lower()) or (isbn and book.isbn == isbn) :
                return book
        return None
    
    """Save books to JSON"""
    def save_to_json(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self._books],
                      f, ensure_ascii=False, indent=4)

    """ Loads books from the JSON based on their type"""
    def load_from_json(self, filename: str):
        if not os.path.exists(filename):
            return  # No file yet, nothing to load

        with open(filename, "r", encoding="utf-8") as f:
            books_data = json.load(f)
            
        self._books.clear()
        for data in books_data:
            book_type = data.get("type", "Book")
            if book_type == "EBook":
                book = EBook(data["title"], data["author"], data["isbn"], data["file_format"])
            elif book_type == "AudioBook":
                book = AudioBook(data["title"], data["author"], data["isbn"], data["duration"])
            else:
                book = Book(data["title"], data["author"], data["isbn"])
            if data.get("is_borrowed"):
                book.is_borrowed = True
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

