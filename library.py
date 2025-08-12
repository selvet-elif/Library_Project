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

    # Finds a book by its title or its ISBN number.
    def find_book(self, title: str = None, isbn: str = None) -> Book | None:
        for book in self._books:
            if book.title.lower() == title.lower() or book.isbn == isbn :
                return book
        return None
    
    # Gives the book list.
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
    
@dataclass
class Member:
    """Represents a library member using dataclasses."""
    name: str
    member_id: int
    borrowed_books: List[Book] = field(default_factory=list)


class PydanticBook(BaseModel):
    """Book model with Pydantic validation."""
    title: str
    author: str
    isbn: str = Field(..., min_length=10, max_length=13)
    publication_year: int = Field(..., gt=1400)  # 1400'den büyük olmalı


def main():
    """Demo function to show the library system in action."""
    print("=== Kütüphane Sistemi Demo ===\n")

    # Create different types of books
    ebook = EBook("1984", "George Orwell", "978-0451524935", "EPUB")
    audio_book = AudioBook("Becoming", "Michelle Obama", "978-1524763138", 780)
    regular_book = Book("The Lord of the Rings", "J.R.R. Tolkien", "978-0618640157")

    print(f"{ebook.title} formatı: {ebook.file_format}")
    print(f"{audio_book.title} süresi: {audio_book.duration} dakika\n")

    # Create library and add books (Composition)
    my_library = Library(name="City Library")
    my_library.add_book(ebook)
    my_library.add_book(audio_book)
    my_library.add_book(regular_book)

    print(f"{my_library.name} kütüphanesindeki toplam kitap sayısı: {my_library.total_books}")

    # Book list SE
    book_list = my_library.list_books()
    print(f"Kitap listesi\n{book_list}")
    
    # Find a book
    found_book = my_library.find_book("1984")
    if found_book:
        print(f"Bulunan kitap: {found_book.title} by {found_book.author}\n")

    # Demonstrate Polymorphism
    print("=== Polimorfizm Örneği ===")
    book_list = [regular_book, ebook, audio_book]

    for book in book_list:
        print(book.display_info())

    print("\n=== Dataclass Örneği ===")
    # Create a member using dataclasses
    member1 = Member(name="Alice", member_id=101)
    print(member1)

    print("\n=== Pydantic Doğrulama Örneği ===")
    # Pydantic validation example
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
            isbn="123",  # Çok kısa
            publication_year=1300  # gt=1400 kuralına aykırı
        )
    except ValidationError as e:
        print("Doğrulama beklendiği gibi başarısız oldu:")
        print(e)


if __name__ == "__main__":
    main()