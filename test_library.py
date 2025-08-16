import pytest
from library import Book, EBook, AudioBook, Library, Member, PydanticBook
from pydantic import ValidationError

"""With @pytest.fixtures to ensured that the 
data required for the test was used fresh in each test."""

@pytest.fixture
def sample_book():
    return Book("1984", "George Orwell", "9780451524935")


@pytest.fixture
def sample_ebook():
    return EBook("Dune", "Frank Herbert", "9780441013593", "PDF")


@pytest.fixture
def sample_audiobook():
    return AudioBook("Becoming", "Michelle Obama", "9781524763138", 780)


@pytest.fixture
def temp_library(tmp_path):
    lib_file = tmp_path / "test_library.json"
    return Library(name="Test Library", json_path=str(lib_file))


def test_book_str(sample_book):
    assert "Title: 1984" in str(sample_book)
    assert "Borrowed: No" in str(sample_book)


def test_borrow_and_return_book(sample_book):
    sample_book.borrow_book()
    assert sample_book.is_borrowed is True

    with pytest.raises(ValueError):
        sample_book.borrow_book()

    sample_book.return_book()
    assert sample_book.is_borrowed is False

    with pytest.raises(ValueError):
        sample_book.return_book()


def test_display_info(sample_book, sample_ebook, sample_audiobook):
    assert sample_book.display_info() == "'1984' by George Orwell"
    assert "Format: PDF" in sample_ebook.display_info()
    assert "Duration: 780 minutes" in sample_audiobook.display_info()


def test_to_dict_includes_fields(sample_ebook, sample_audiobook):
    ebook_dict = sample_ebook.to_dict()
    assert ebook_dict["file_format"] == "PDF"

    audio_dict = sample_audiobook.to_dict()
    assert audio_dict["duration"] == 780


def test_library_add_and_list(temp_library, sample_book):
    temp_library.add_book(sample_book)
    assert temp_library.total_books == 1
    assert sample_book.display_info() in temp_library.list_books()


def test_library_does_not_add_duplicate(temp_library, sample_book):
    temp_library.add_book(sample_book)
    temp_library.add_book(sample_book)  # same ISBN
    assert temp_library.total_books == 1


def test_library_find_book(temp_library, sample_book):
    temp_library.add_book(sample_book)
    found = temp_library.find_book(title="1984")
    assert found is sample_book

    not_found = temp_library.find_book(title="Nonexistent")
    assert not_found is None


"""def test_library_save_and_load(temp_library, sample_ebook):
    temp_library.add_book(sample_ebook)
    temp_library.save_to_json(temp_library.json_path)

    # create new library instance and load from file
    new_lib = Library(name="Reloaded", json_path=temp_library.json_path)
    assert new_lib.total_books == 1
    loaded_book = new_lib.find_book(isbn=sample_ebook.isbn)
    assert isinstance(loaded_book, EBook)
    assert loaded_book.file_format == "PDF"""


def test_member_dataclass(sample_book):
    member = Member(name="Alice", member_id=1)
    assert member.name == "Alice"
    assert member.member_id == 1
    assert isinstance(member.borrowed_books, list)
    assert member.borrowed_books == []


def test_pydantic_book_valid():
    valid_book = PydanticBook(
        title="Dune",
        author="Frank Herbert",
        isbn="9780441013593",
        publication_year=1965
    )
    assert valid_book.title == "Dune"


def test_pydantic_book_invalid():
    with pytest.raises(ValidationError):
        PydanticBook(
            title="Bad Book",
            author="Bad Author",
            isbn="123",  # invalid
            publication_year=1300  # too early
        )
