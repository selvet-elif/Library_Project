
import pytest
import httpx
from unittest.mock import patch

from app.models import Book
from openlibrary import fetch_book_from_api


class MockResponse:
    def __init__(self, status_code: int, payload: dict | None = None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


@pytest.mark.asyncio
async def test_fetch_book_success():
    isbn = "1234567890"

    book_data = {"title": "Test Kitap", "authors": [{"key": "/authors/OL123A"}]}
    author_data = {"name": "Test Yazar"}

    async def mock_get(self, url, timeout=10.0):
        if url == f"https://openlibrary.org/isbn/{isbn}.json":
            return MockResponse(200, book_data)
        elif url == "https://openlibrary.org/authors/OL123A.json":
            return MockResponse(200, author_data)
        return MockResponse(404, {})

    with patch("httpx.AsyncClient.get", new=mock_get):
        book = await fetch_book_from_api(isbn)
        assert isinstance(book, Book)
        assert book.title == "Test Kitap"
        assert book.author == "Test Yazar"
        assert book.isbn == isbn


@pytest.mark.asyncio
async def test_fetch_book_not_found():
    isbn = "0000000000"

    async def mock_get(self, url, timeout=10.0):
        return MockResponse(404, {})

    with patch("httpx.AsyncClient.get", new=mock_get):
        with pytest.raises(ValueError, match="Kitap bulunamadı"):
            await fetch_book_from_api(isbn)


@pytest.mark.asyncio
async def test_fetch_book_connection_error():
    isbn = "1234567890"

    async def mock_get(self, url, timeout=10.0):
        raise httpx.RequestError("No connection")

    with patch("httpx.AsyncClient.get", new=mock_get):
        with pytest.raises(ValueError, match="İnternet bağlantısı yok veya API'ye ulaşılamıyor"):
            await fetch_book_from_api(isbn)
