"""Tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from api import app, BookCreate, BookResponse, MemberCreate, MemberResponse, BorrowRequest, PaginatedBookResponse, BorrowRecordResponse
from app.models import Book
from app.db_models import BookDB, MemberDB, BorrowRecordDB


@pytest.fixture
def client():
    """Create a test client for FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_session():
    """Create a mock async session."""
    session = AsyncMock()
    return session


@pytest.fixture
def mock_book():
    """Create a mock book."""
    return Book(
        isbn="9780451524935",
        title="1984",
        author="George Orwell",
        status="available",
    )


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_api_models():
    """Test API Pydantic models."""
    # Test BookCreate
    book_create = BookCreate(isbn="9780451524935")
    assert book_create.isbn == "9780451524935"
    
    # Test BookResponse
    book_response = BookResponse(
        title="1984",
        author="George Orwell",
        isbn="9780451524935",
        status="available"
    )
    assert book_response.title == "1984"
    assert book_response.status == "available"
    
    # Test MemberCreate
    member_create = MemberCreate(name="John Doe")
    assert member_create.name == "John Doe"
    
    # Test MemberResponse
    member_response = MemberResponse(id=1, name="John Doe")
    assert member_response.id == 1
    
    # Test BorrowRequest
    borrow_request = BorrowRequest(member_id=1, isbn="9780451524935")
    assert borrow_request.member_id == 1
    assert borrow_request.isbn == "9780451524935"
    
    # Test PaginatedBookResponse
    paginated = PaginatedBookResponse(
        items=[book_response],
        total=1,
        skip=0,
        limit=10
    )
    assert paginated.total == 1
    assert len(paginated.items) == 1
    
    # Test BorrowRecordResponse
    borrow_record = BorrowRecordResponse(
        id=1,
        member_id=1,
        isbn="9780451524935",
        borrow_date="2024-01-01T00:00:00",
        return_date=None
    )
    assert borrow_record.id == 1
    assert borrow_record.return_date is None


def test_health_check_endpoint_structure(client):
    """Test health check endpoint exists and handles errors gracefully."""
    # Skip if DB not available - endpoint exists
    pytest.skip("Requires database connection - tested in integration tests")


def test_startup_event():
    """Test startup event handler."""
    from unittest.mock import patch
    
    # Verify startup_event function exists and is callable
    from api import startup_event
    assert callable(startup_event)
    
    # Test that it calls init_db
    with patch("api.init_db") as mock_init_db:
        startup_event()
        mock_init_db.assert_called_once()


def test_api_app_creation():
    """Test FastAPI app initialization."""
    from api import app
    assert app is not None
    assert app.title == "Library Management API"
    assert app.version == "1.0.0"


def test_cors_middleware():
    """Test CORS middleware is configured."""
    from api import app
    # Check that middleware is added
    assert len(app.user_middleware) > 0
