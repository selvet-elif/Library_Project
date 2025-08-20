
import pytest
import httpx
from unittest.mock import patch, MagicMock
from openlibrary import fetch_book_from_api, Book  

def test_fetch_book_success():
    isbn = "1234567890"
    
    book_data = {"title": "Test Kitap", "authors": [{"key": "/authors/OL123A"}]}
    author_data = {"name": "Test Yazar"}

    # Mocked httpx.get
    def mock_get(url, timeout):
        mock_resp = MagicMock()
        if url == f"https://openlibrary.org/isbn/{isbn}.json":
            mock_resp.status_code = 200
            mock_resp.json.return_value = book_data
        elif url == "https://openlibrary.org/authors/OL123A.json":
            mock_resp.status_code = 200
            mock_resp.json.return_value = author_data
        return mock_resp

    with patch("httpx.get", new=mock_get):
        book = fetch_book_from_api(isbn)
        assert isinstance(book, Book)
        assert book.title == "Test Kitap"
        assert book.author == "Test Yazar"
        assert book.isbn == isbn

def test_fetch_book_not_found():
    isbn = "0000000000"

    def mock_get(url, timeout):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        return mock_resp

    with patch("httpx.get", new=mock_get):
        with pytest.raises(ValueError, match="Kitap bulunamadı"):
            fetch_book_from_api(isbn)

def test_fetch_book_connection_error():
    isbn = "1234567890"

    def mock_get(url, timeout):
        raise httpx.RequestError("No connection")

    with patch("httpx.get", new=mock_get):
        with pytest.raises(ValueError, match="İnternet bağlantısı yok veya API'ye ulaşılamıyor"):
            fetch_book_from_api(isbn)
