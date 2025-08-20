import httpx

def get_book_by_isbn(isbn: str) -> dict | None:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            key = f"ISBN:{isbn}"
            if key in data:
                book_info = data[key]
                title = book_info.get("title")
                authors = [a["name"] for a in book_info.get("authors", [])]
                return {"title": title, "authors": authors}
            else:
                print("Kitap bulunamadı.")
        except httpx.RequestError:
            print("Bağlantı hatası veya API erişilemiyor.")
        return None