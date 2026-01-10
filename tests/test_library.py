"""Tests for Library class (JSON-based persistence)."""
import pytest
import json
import os
from pydantic import ValidationError

from app.models import Book
from library import AudioBook, EBook, Library, Member, PydanticBook


@pytest.fixture
def sample_book():
    """Create a sample Book."""
    return Book(title="1984", author="George Orwell", isbn="9780451524935")


@pytest.fixture
def sample_ebook():
    """Create a sample EBook."""
    return EBook(title="Dune", author="Frank Herbert", isbn="9780441013593", file_format="PDF")


@pytest.fixture
def sample_audiobook():
    """Create a sample AudioBook."""
    return AudioBook(title="Becoming", author="Michelle Obama", isbn="9781524763138", duration=780)


@pytest.fixture
def temp_library(tmp_path):
    """Create a temporary Library instance."""
    lib_file = tmp_path / "test_library.json"
    return Library(name="Test Library", json_path=str(lib_file))


def test_ebook_display_info(sample_ebook):
    """Test EBook display_info method."""
    info = sample_ebook.display_info()
    assert "Dune" in info
    assert "Frank Herbert" in info
    assert "Format: PDF" in info


def test_audiobook_display_info(sample_audiobook):
    """Test AudioBook display_info method."""
    info = sample_audiobook.display_info()
    assert "Becoming" in info
    assert "Michelle Obama" in info
    assert "Duration: 780 minutes" in info


def test_library_add_book(temp_library, sample_book):
    """Test adding a book to the library."""
    result = temp_library.add_book(sample_book)
    assert result is True
    assert temp_library.total_books == 1
    assert sample_book.display_info() in temp_library.list_books()


def test_library_does_not_add_duplicate(temp_library, sample_book):
    """Test that duplicate books are not added."""
    temp_library.add_book(sample_book)
    result = temp_library.add_book(sample_book)  # same ISBN
    assert result is False
    assert temp_library.total_books == 1


def test_library_delete_book(temp_library, sample_book):
    """Test deleting a book from the library."""
    temp_library.add_book(sample_book)
    result = temp_library.delete_book(sample_book.isbn)
    assert result is True
    assert temp_library.total_books == 0


def test_library_delete_nonexistent_book(temp_library):
    """Test deleting a book that doesn't exist."""
    result = temp_library.delete_book("nonexistent")
    assert result is False


def test_library_find_book_by_title(temp_library, sample_book):
    """Test finding a book by title."""
    temp_library.add_book(sample_book)
    found = temp_library.find_book(title="1984")
    assert found is not None
    assert found.isbn == sample_book.isbn


def test_library_find_book_by_isbn(temp_library, sample_book):
    """Test finding a book by ISBN."""
    temp_library.add_book(sample_book)
    found = temp_library.find_book(isbn=sample_book.isbn)
    assert found is not None
    assert found.title == sample_book.title


def test_library_find_book_case_insensitive(temp_library, sample_book):
    """Test finding a book with case-insensitive title search."""
    temp_library.add_book(sample_book)
    found = temp_library.find_book(title="1984".upper())
    assert found is not None


def test_library_find_book_not_found(temp_library):
    """Test finding a book that doesn't exist."""
    found = temp_library.find_book(title="Nonexistent")
    assert found is None


def test_library_get_books(temp_library, sample_book):
    """Test getting all books as domain models."""
    temp_library.add_book(sample_book)
    books = temp_library.get_books()
    assert len(books) == 1
    assert books[0] == sample_book
    assert isinstance(books[0], Book)


def test_library_list_books(temp_library, sample_book):
    """Test listing books as display strings."""
    temp_library.add_book(sample_book)
    book_list = temp_library.list_books()
    assert len(book_list) == 1
    assert sample_book.display_info() in book_list


def test_library_save_and_load_json(temp_library, sample_ebook):
    """Test saving and loading library from JSON."""
    temp_library.add_book(sample_ebook)
    temp_library.save_to_json(temp_library.json_path)

    # Verify file exists
    assert os.path.exists(temp_library.json_path)

    # Load from file
    new_lib = Library(name="Reloaded", json_path=temp_library.json_path)
    assert new_lib.total_books == 1
    loaded_book = new_lib.find_book(isbn=sample_ebook.isbn)
    assert isinstance(loaded_book, EBook)
    assert loaded_book.file_format == "PDF"


def test_library_load_nonexistent_file(tmp_path):
    """Test loading library when JSON file doesn't exist."""
    lib_file = tmp_path / "nonexistent.json"
    library = Library(name="New Library", json_path=str(lib_file))
    assert library.total_books == 0


def test_library_total_books_property(temp_library, sample_book):
    """Test total_books property."""
    assert temp_library.total_books == 0
    temp_library.add_book(sample_book)
    assert temp_library.total_books == 1


def test_member_dataclass():
    """Test Member dataclass creation."""
    member = Member(name="Alice", member_id=1)
    assert member.name == "Alice"
    assert member.member_id == 1
    assert isinstance(member.borrowed_books, list)
    assert member.borrowed_books == []


def test_pydantic_book_valid():
    """Test creating a valid PydanticBook."""
    valid_book = PydanticBook(
        title="Dune",
        author="Frank Herbert",
        isbn="9780441013593",
        publication_year=1965,
    )
    assert valid_book.title == "Dune"
    assert valid_book.author == "Frank Herbert"
    assert valid_book.isbn == "9780441013593"
    assert valid_book.publication_year == 1965


def test_pydantic_book_invalid_isbn():
    """Test PydanticBook validation with invalid ISBN."""
    with pytest.raises(ValidationError):
        PydanticBook(
            title="Bad Book",
            author="Bad Author",
            isbn="123",  # invalid - too short
            publication_year=1965,
        )


def test_pydantic_book_invalid_year():
    """Test PydanticBook validation with invalid publication year."""
    with pytest.raises(ValidationError):
        PydanticBook(
            title="Bad Book",
            author="Bad Author",
            isbn="9780441013593",
            publication_year=1300,  # too early
        )


def test_library_name_property(temp_library):
    """Test library name property."""
    assert temp_library.name == "Test Library"


def test_library_save_empty(temp_library, tmp_path):
    """Test saving empty library."""
    temp_library.save_to_json(temp_library.json_path)
    assert os.path.exists(temp_library.json_path)
    
    # Verify JSON file structure
    with open(temp_library.json_path, 'r') as f:
        data = json.load(f)
        assert data == []


def test_library_load_with_audiobook(tmp_path, sample_audiobook):
    """Test loading library with AudioBook type."""
    lib_file = tmp_path / "test_audiobook.json"
    library = Library(name="Test", json_path=str(lib_file))
    library.add_book(sample_audiobook)
    library.save_to_json(lib_file)
    
    # Create new library and load
    new_lib = Library(name="Reloaded", json_path=str(lib_file))
    assert new_lib.total_books == 1
    loaded_book = new_lib.find_book(isbn=sample_audiobook.isbn)
    assert isinstance(loaded_book, AudioBook)
    assert loaded_book.duration == 780


def test_library_load_with_regular_book(tmp_path, sample_book):
    """Test loading library with regular Book type."""
    lib_file = tmp_path / "test_regular.json"
    library = Library(name="Test", json_path=str(lib_file))
    library.add_book(sample_book)
    library.save_to_json(lib_file)
    
    # Create new library and load
    new_lib = Library(name="Reloaded", json_path=str(lib_file))
    assert new_lib.total_books == 1
    loaded_book = new_lib.find_book(isbn=sample_book.isbn)
    assert isinstance(loaded_book, Book)
    assert loaded_book.title == sample_book.title


def test_book_display_info(sample_book):
    """Test Book display_info method."""
    info = sample_book.display_info()
    assert info == "'1984' by George Orwell"
