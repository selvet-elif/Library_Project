from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from openlibrary import fetch_book_from_api
from library import Library  # Import Library class

app = FastAPI(
    title="Library Management API",
    description="A simple library management system API",
    version="1.0.0"
)

# Pydantic modelleri
class BookCreate(BaseModel):
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

# Library instance
library = Library("library.json")

@app.get("/")
async def root():
    return {"message": "Library Management API'ye hoş geldiniz!"}

@app.get("/books", response_model=List[BookResponse])
async def get_books():
    """Tüm kitapları listeler"""
    return library.get_books()

@app.post("/books", response_model=BookResponse)
async def add_book(book_create: BookCreate):
    """ISBN ile yeni kitap ekler"""
    try:
        # API'den kitap bilgilerini al
        book_data = await fetch_book_from_api(book_create.isbn)
        
        # Aynı ISBN kontrolü
        if any(book["isbn"] == book_create.isbn for book in library.get_books()):
            raise HTTPException(status_code=400, detail="Bu ISBN zaten mevcut")
        
        # Yeni kitabı ekle
        new_book = {
            "title": book_data.title,
            "author": book_data.author,
            "isbn": book_data.isbn
        }
        library.add_book(new_book)
        
        return new_book
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/{isbn}", response_model=BookResponse)
async def get_book(isbn: str):
    """ISBN ile belirli bir kitabı getirir"""
    book = library.get_book_by_isbn(isbn)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Kitap bulunamadı")

@app.delete("/books/{isbn}")
async def delete_book(isbn: str):
    """ISBN ile kitabı siler"""
    result = library.delete_book(isbn)
    if not result:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    return {"message": "Kitap silindi"}

@app.get("/health")
async def health_check():
    """API sağlık durumu"""
    books = library.get_books()
    return {"status": "healthy", "books_count": len(books)}

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
