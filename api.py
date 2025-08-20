# api.py
# FastAPI app + helper to fetch books from OpenLibrary
# Add the following lines to your requirements.txt:
# fastapi
# uvicorn
# httpx
# pytest
# (pydantic is a dependency of fastapi but you can list it explicitly if you want)

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import re

app = FastAPI(title="Library API")


def _clean_isbn(isbn: str) -> str:
    # remove hyphens and whitespace
    return re.sub(r"[^0-9Xx]", "", isbn)


async def _fetch_openlibrary(isbn: str) -> Optional[dict]:
    """Internal async fetch helper (not used directly by tests which mock httpx.get).
    Returns dict with keys: title, authors (list of names) or None on failure.
    """
    clean = _clean_isbn(isbn)
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{clean}&format=json&jscmd=data"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return None

    key = f"ISBN:{clean}"
    if key not in data:
        return None

    entry = data[key]
    title = entry.get("title", "Unknown Title")
    authors = entry.get("authors", [])
    # Normalize authors: could be list of dicts with 'name' or list of strings
    names: List[str] = []
    for a in authors:
        if isinstance(a, dict):
            names.append(a.get("name", "Unknown"))
        elif isinstance(a, str):
            names.append(a)
    return {"title": title, "authors": names}


# The tests expect a synchronous get_book_by_isbn that uses httpx.get and returns
# a dict like {"title": ..., "authors": [...] } or None on error. We'll provide
# that function for compatibility with the existing test suite and library module.

def get_book_by_isbn(isbn: str) -> Optional[dict]:
    """Synchronous helper used by Library.add_book and by tests.
    Uses httpx.get (sync) so tests can mock httpx.get easily.
    """
    clean = _clean_isbn(isbn)
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{clean}&format=json&jscmd=data"
    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None

    key = f"ISBN:{clean}"
    if key not in data:
        return None

    entry = data[key]
    title = entry.get("title", "Unknown Title")
    authors = entry.get("authors", [])
    names: List[str] = []
    for a in authors:
        if isinstance(a, dict):
            names.append(a.get("name", "Unknown"))
        elif isinstance(a, str):
            names.append(a)
    return {"title": title, "authors": names}


# Pydantic models for request/response
class ISBNRequest(BaseModel):
    isbn: str


class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str
    is_borrowed: bool = False


# Lazy-loaded Library singleton to avoid circular imports (library.py imports
# get_book_by_isbn at module import time). We import Library only when needed.
_library_instance = None


def get_library():
    global _library_instance
    if _library_instance is None:
        # import here to avoid circular import at module-import time
        from library import Library
        _library_instance = Library(name="City Library")
    return _library_instance


@app.get("/", tags=["root"])  # simple root for quick check
def read_root():
    return {"message": "Library API is running. Visit /docs for interactive API docs."}


@app.get("/books", response_model=List[BookResponse])
def list_books():
    lib = get_library()
    books = []
    for b in lib._books:  # using internal list for serialization
        books.append(BookResponse(title=b.title, author=b.author, isbn=b.isbn, is_borrowed=b.is_borrowed))
    return books


@app.post("/books", response_model=BookResponse)
def add_book(payload: ISBNRequest):
    lib = get_library()
    isbn = payload.isbn
    added = lib.add_book(isbn)
    if not added:
        # Try to give a helpful error if the book wasn't found or already exists
        # Check if book exists
        if any(book.isbn == isbn for book in lib._books):
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists in library.")
        else:
            raise HTTPException(status_code=400, detail="Book could not be fetched from OpenLibrary or an error occurred.")
    # Find the added book and return it
    for b in lib._books:
        if b.isbn == isbn:
            return BookResponse(title=b.title, author=b.author, isbn=b.isbn, is_borrowed=b.is_borrowed)
    # Fallback (shouldn't happen)
    raise HTTPException(status_code=500, detail="Book added but could not be retrieved.")


@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    lib = get_library()
    success = lib.delete_book(isbn)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )