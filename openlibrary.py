import httpx


class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = str(isbn)
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


def fetch_book_from_api(isbn: str) -> Book:
    """Fetch book info from OpenLibraryAPI"""
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    
    try:
        response = httpx.get(url, timeout=10.0)
        
        if response.status_code == 404:
            raise ValueError("Kitap bulunamadı")
            
        response.raise_for_status()
        data = response.json()
        
        title = data.get("title", "Bilinmeyen Başlık")
        
        authors = data.get("authors", [])
        author_name = "Bilinmeyen Yazar"
        
        if authors:
            author_key = authors[0].get("key", "")
            if author_key:
                try:
                    author_url = f"https://openlibrary.org{author_key}.json"
                    author_response = httpx.get(author_url, timeout=5.0)
                    author_data = author_response.json()
                    author_name = author_data.get("name", "Bilinmeyen Yazar")
                except:
                    author_name = "Bilinmeyen Yazar"
        
        return Book(title=title, author=author_name, isbn=isbn)
    
    except httpx.RequestError:
        raise ValueError("İnternet bağlantısı yok veya API'ye ulaşılamıyor")
    except Exception as e:
        raise ValueError(f"Beklenmeyen hata: {str(e)}")
