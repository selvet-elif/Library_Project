from typing import List
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, ValidationError
import json
import os

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
    """Adds a new book. If the book existed it doesn't add it to the library."""
    def add_book(self, book: Book):
        for existing_books in self._books:
            if existing_books.isbn == book.isbn:
                return
            
        self._books.append(book)
        self.save_to_json(self.json_path)  # To automatically saving new books to JSON.

    def list_books(self):
        return [book.display_info() for book in self._books]

    """Finds a book by its title or its ISBN number."""
    def find_book(self, title: str = None, isbn: str = None) -> Book | None:
        for book in self._books:
            if (book and book.title.lower() == title.lower()) or (isbn and book.isbn == isbn) :
                return book
        return None
    
    """Save and Load books to/from JSON"""
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


def main():
    print("=== Kütüphane Sistemi Demo ===\n")

    # Create books
    ebook = EBook("1984", "George Orwell", "9780451524935", "EPUB")
    audio_book = AudioBook("Becoming", "Michelle Obama", "9781524763138", 780)
    regular_book = Book("The Lord of the Rings", "J.R.R. Tolkien", "9780618640157")

    # Create library and add books
    my_library = Library(name="City Library")
    my_library.add_book(ebook)
    my_library.add_book(audio_book)
    my_library.add_book(regular_book)
    my_library.save_to_json(my_library.json_path)
    print(f"{my_library.name} kütüphanesindeki toplam kitap sayısı: {my_library.total_books}\n")

    # List books
    print("Kitap listesi:")
    for info in my_library.list_books():
        print("-", info)

    # Find a book
    found_book = my_library.find_book(title="1984")
    if found_book:
        print(f"\nBulunan kitap: {found_book.display_info()}")

    # Demonstrate polymorphism
    print("\n=== Polimorfizm Örneği ===")
    for book in [regular_book, ebook, audio_book]:
        print(book.display_info())

    # Dataclass example
    print("\n=== Dataclass Örneği ===")
    member1 = Member(name="Alice", member_id=101)
    print(member1)

    # Pydantic validation
    print("\n=== Pydantic Doğrulama Örneği ===")
    try:
        valid_book = PydanticBook(
            title="Dune",
            author="Frank Herbert",
            isbn="9780441013593",
            publication_year=1965
        )
        print("Geçerli kitap başarıyla oluşturuldu:")
        print(valid_book.model_dump_json(indent=2))
    except ValidationError as e:
        print(e)

    print("\n--- Geçersiz bir kitap oluşturma denemesi ---")
    try:
        invalid_book = PydanticBook(
            title="Invalid Book",
            author="Bad Author",
            isbn="123",  # Too short
            publication_year=1300  # It's against the gt=1400 rule
        )
    except ValidationError as e:
        print("Doğrulama beklendiği gibi başarısız oldu:")
        print(e)


if __name__ == "__main__":
    main()