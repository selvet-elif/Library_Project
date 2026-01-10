"""Tests for OpenLibrary client."""
import pytest
import httpx
from unittest.mock import patch, AsyncMock

from app.models import Book
from openlibrary import fetch_book_from_api


class MockResponse:
    """Mock HTTP response for testing."""
    def __init__(self, status_code: int, payload: dict | None = None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("Error", request=None, response=self)
        return None


@pytest.mark.asyncio
async def test_fetch_book_success():
    """Test successfully fetching a book from OpenLibrary API."""
    isbn = "1234567890"
    
    book_data = {"title": "Test Kitap", "authors": [{"key": "/authors/OL123A"}]}
    author_data = {"name": "Test Yazar"}

    async def mock_get(url, **kwargs):
        if url == f"https://openlibrary.org/isbn/{isbn}.json":
            response = MockResponse(200, book_data)
            return response
        elif url == "https://openlibrary.org/authors/OL123A.json":
            response = MockResponse(200, author_data)
            return response
        return MockResponse(404, {})

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                book = await fetch_book_from_api(isbn)
                assert isinstance(book, Book)
                assert book.title == "Test Kitap"
                assert book.author == "Test Yazar"
                assert book.isbn == isbn


@pytest.mark.asyncio
async def test_fetch_book_no_author_key():
    """Test fetching a book when author key is missing."""
    isbn = "1234567890"
    book_data = {"title": "Test Kitap", "authors": [{}]}

    async def mock_get(url, **kwargs):
        if url == f"https://openlibrary.org/isbn/{isbn}.json":
            return MockResponse(200, book_data)
        return MockResponse(404, {})

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                book = await fetch_book_from_api(isbn)
                assert book.title == "Test Kitap"
                assert book.author == "Bilinmeyen Yazar"


@pytest.mark.asyncio
async def test_fetch_book_no_authors():
    """Test fetching a book when authors field is missing."""
    isbn = "1234567890"
    book_data = {"title": "Test Kitap"}

    async def mock_get(url, **kwargs):
        if url == f"https://openlibrary.org/isbn/{isbn}.json":
            return MockResponse(200, book_data)
        return MockResponse(404, {})

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                book = await fetch_book_from_api(isbn)
                assert book.title == "Test Kitap"
                assert book.author == "Bilinmeyen Yazar"


@pytest.mark.asyncio
async def test_fetch_book_author_fetch_fails():
    """Test when author details fetch fails."""
    isbn = "1234567890"
    book_data = {"title": "Test Kitap", "authors": [{"key": "/authors/OL123A"}]}

    async def mock_get(url, **kwargs):
        if url == f"https://openlibrary.org/isbn/{isbn}.json":
            return MockResponse(200, book_data)
        elif "/authors/" in url:
            raise Exception("Author fetch failed")
        return MockResponse(404, {})

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                book = await fetch_book_from_api(isbn)
                assert book.title == "Test Kitap"
                assert book.author == "Bilinmeyen Yazar"


@pytest.mark.asyncio
async def test_fetch_book_not_found():
    """Test fetching a book that doesn't exist."""
    isbn = "0000000000"

    async def mock_get(url, **kwargs):
        return MockResponse(404, {})

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                with pytest.raises(ValueError, match="Kitap bulunamadı"):
                    await fetch_book_from_api(isbn)


@pytest.mark.asyncio
async def test_fetch_book_connection_error():
    """Test handling connection errors."""
    isbn = "1234567890"

    async def mock_get(url, **kwargs):
        raise httpx.RequestError("No connection")

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                with pytest.raises(ValueError, match="İnternet bağlantısı yok veya API'ye ulaşılamıyor"):
                    await fetch_book_from_api(isbn)


@pytest.mark.asyncio
async def test_fetch_book_http_error():
    """Test handling HTTP errors."""
    isbn = "1234567890"

    async def mock_get(url, **kwargs):
        response = MockResponse(500, {})
        response.raise_for_status()  # This will raise HTTPStatusError
        return response

    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        with patch("httpx.AsyncClient.__aenter__", return_value=AsyncMock(get=mock_get)):
            with patch("httpx.AsyncClient.__aexit__", return_value=None):
                with pytest.raises(ValueError):
                    await fetch_book_from_api(isbn)
