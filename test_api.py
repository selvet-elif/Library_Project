import pytest
import httpx
from api import get_book_by_isbn 

def test_get_book_by_isbn_success(mocker):
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "ISBN:1234567890": {
            "title": "Test Book",
            "authors": [{"name": "Author One"}, {"name": "Author Two"}]
        }
    }
    mock_response.raise_for_status.return_value = None
    mocker.patch("httpx.get", return_value=mock_response)

    result = get_book_by_isbn("1234567890")
    assert result == {
        "title": "Test Book",
        "authors": ["Author One", "Author Two"]
    }

def test_get_book_by_isbn_not_found(mocker):
    # Book didn't found
    mock_response = mocker.Mock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None
    mocker.patch("httpx.get", return_value=mock_response)

    result = get_book_by_isbn("0000000000")
    assert result is None

def test_get_book_by_isbn_request_error(mocker):
    # Network error
    mocker.patch("httpx.get", side_effect=httpx.RequestError("Connection Error"))

    result = get_book_by_isbn("1234567890")
    assert result is None
