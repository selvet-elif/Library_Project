from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
from openlibrary import fetch_book_from_api

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

# JSON veritabanı yönetimi
def load_books():
    try:
        with open("library.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_books(books):
    with open("library.json", "w") as f:
        json.dump(books, f, indent=2)

@app.get("/")
async def root():
    return {"message": "Library Management API'ye hoş geldiniz!"}

@app.get("/books", response_model=List[BookResponse])
async def get_books():
    """Tüm kitapları listeler"""
    return load_books()

@app.post("/books", response_model=BookResponse)
async def add_book(book_create: BookCreate):
    """ISBN ile yeni kitap ekler"""
    try:
        # API'den kitap bilgilerini al
        book_data = await fetch_book_from_api(book_create.isbn)
        
        # Mevcut kitapları yükle
        books = load_books()
        
        # Aynı ISBN kontrolü
        if any(book["isbn"] == book_create.isbn for book in books):
            raise HTTPException(status_code=400, detail="Bu ISBN zaten mevcut")
        
        # Yeni kitabı ekle
        new_book = {
            "title": book_data.title,
            "author": book_data.author,
            "isbn": book_data.isbn
        }
        books.append(new_book)
        
        # Kitapları kaydet
        save_books(books)
        
        return new_book
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/books/{isbn}", response_model=BookResponse)
async def get_book(isbn: str):
    """ISBN ile belirli bir kitabı getirir"""
    books = load_books()
    for book in books:
        if book["isbn"] == isbn:
            return book
    raise HTTPException(status_code=404, detail="Kitap bulunamadı")

@app.delete("/books/{isbn}")
async def delete_book(isbn: str):
    """ISBN ile kitabı siler"""
    books = load_books()
    new_books = [book for book in books if book["isbn"] != isbn]
    
    if len(new_books) == len(books):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")
    
    save_books(new_books)
    return {"message": "Kitap silindi"}

@app.get("/health")
async def health_check():
    """API sağlık durumu"""
    books = load_books()
    return {"status": "healthy", "books_count": len(books)}