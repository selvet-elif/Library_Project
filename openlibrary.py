import httpx
from app.models import Book


async def fetch_book_from_api(isbn: str) -> Book:
    """Fetch book info from OpenLibrary API asynchronously and return a unified Book model."""
    url = f"https://openlibrary.org/isbn/{isbn}.json"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

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
                        author_response = await client.get(author_url, timeout=5.0)
                        author_data = author_response.json()
                        author_name = author_data.get("name", "Bilinmeyen Yazar")
                    except Exception:
                        author_name = "Bilinmeyen Yazar"

        return Book(title=title, author=author_name, isbn=str(isbn))

    except httpx.RequestError:
        raise ValueError("İnternet bağlantısı yok veya API'ye ulaşılamıyor")
    except ValueError:
        # Re-raise domain errors (e.g., not found) without wrapping
        raise
    except Exception as e:
        raise ValueError(f"Beklenmeyen hata: {str(e)}")
