from typing import List
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, ValidationError


class Book:
    # Singe book in the library
    def __init__(self, title: str, author: str, isbn: str, page: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.page = page
        self.is_borrowed = False
        
    def borrow_book(self):
        # Marked the book as borrowed
        if not self.is_borrowed: 
            self.is_borrowed = True
        else:
            # Raise an error if the book already borrowed    
            raise ValueError(f"'{self.title}' ")
    
    def return_book(self):
        # Marks the book as returned.
        if self.is_borrowed:
            self.is_borrowed = False
        else:
            # Raise an error if the book wasn't borrowed for it to be returned.
            raise ValueError(f"'{self.title}' was not borrowed.")

    # To display the book name and it's author.
    def display_info(self) -> str:
        return f"'{self.title}' by {self.author}"
    
    
    
class EBook(Book):
    # An E-Book that inherits from Book.
    def __init__(self, title: str, author: str, isbn: str, file_format: str):
        super().__init__(title, author, isbn)
        self.file_format = file_format

    def display_info(self) -> str:
        return f"{super().display_info()} [Format: {self.file_format}]"


class AudioBook(Book):
    # An Audio book that inherits from Book.
    def __init__(self, title: str, author: str, isbn: str, duration_in_minutes: int):
        super().__init__(title, author, isbn)
        self.duration = duration_in_minutes

    def display_info(self) -> str:
        return f"{super().display_info()} [Duration: {self.duration} minutes.]"
    
    
    

class Library:
    # Manages a collection of books using composition.
    def __init__(self, name: str):
        self.name = name
        # Encapsulation: this list is an internal detail of the class.
        self._books = []

    def add_book(self, book: Book):
        self._books.append(book)

    def find_book(self, title: str) -> Book | None:
        for book in self._books:
            if book.title.lower() == title.lower():
                return book
        return None
    def list_books(self):
        if not self._books:
            return "No avaliable book in the library."
        else:
            for i, book in enumerate(self._books):
                book_list="\n".join(f"{i+1}. {book.title} - {book.author}")
        return book_list
        
        
    @property
    def total_books(self) -> int:
        return len(self._books)