# API Endpoints Documentation

## Complete API Endpoint List

### Books Endpoints

1. **GET /books** - List books with filtering and pagination
   - Query Parameters:
     - `skip` (int, default: 0) - Number of records to skip
     - `limit` (int, default: 100, max: 1000) - Maximum records to return
     - `author` (string, optional) - Filter by author (partial match)
     - `title` (string, optional) - Filter by title (partial match)
     - `status` (string, optional) - Filter by status (available, borrowed)
   - Response: `PaginatedBookResponse` with items, total, skip, limit

2. **POST /books** - Add a book by ISBN
   - Body: `{"isbn": "string"}`
   - Response: `BookResponse`

3. **GET /books/{isbn}** - Get book by ISBN
   - Response: `BookResponse`

4. **DELETE /books/{isbn}** - Delete a book
   - Response: `{"message": "Kitap silindi"}`

5. **GET /books/{isbn}/borrows** - Get borrow history for a book
   - Query Parameters:
     - `active_only` (bool, default: false) - Show only active borrows
   - Response: `List[BorrowRecordResponse]`

### Members Endpoints

6. **POST /members** - Create a new member
   - Body: `{"name": "string"}`
   - Response: `MemberResponse`

7. **GET /members** - List all members
   - Query Parameters:
     - `skip` (int, default: 0)
     - `limit` (int, default: 100, max: 1000)
   - Response: `List[MemberResponse]`

8. **GET /members/{member_id}** - Get member details
   - Response: `MemberResponse`

9. **GET /members/{member_id}/borrows** - Get member's borrow history
   - Query Parameters:
     - `active_only` (bool, default: false) - Show only active borrows
   - Response: `List[BorrowRecordResponse]`

### Borrowing Endpoints

10. **POST /borrow** - Borrow a book
    - Body: `{"member_id": int, "isbn": "string"}`
    - Response: `{"message": "Kitap başarıyla ödünç alındı"}`

11. **POST /return** - Return a book
    - Body: `{"member_id": int, "isbn": "string"}`
    - Response: `{"message": "Kitap başarıyla iade edildi"}`

### System Endpoints

12. **GET /health** - Health check
    - Response: `{"status": "healthy", "books_count": int}`

13. **GET /** - Welcome message
    - Response: `{"message": "Library Management API'ye hoş geldiniz!"}`

## Response Models

### BookResponse
```json
{
  "title": "string",
  "author": "string",
  "isbn": "string",
  "status": "available" | "borrowed"
}
```

### PaginatedBookResponse
```json
{
  "items": [BookResponse],
  "total": int,
  "skip": int,
  "limit": int
}
```

### MemberResponse
```json
{
  "id": int,
  "name": "string"
}
```

### BorrowRecordResponse
```json
{
  "id": int,
  "member_id": int,
  "isbn": "string",
  "borrow_date": "ISO8601 string",
  "return_date": "ISO8601 string" | null
}
```

## Example Usage

### Filter Available Books by Author
```bash
curl "http://localhost:8000/books?author=Orwell&status=available&skip=0&limit=10"
```

### Get Member's Active Borrows
```bash
curl "http://localhost:8000/members/1/borrows?active_only=true"
```

### Borrow a Book
```bash
curl -X POST "http://localhost:8000/borrow" \
  -H "Content-Type: application/json" \
  -d '{"member_id": 1, "isbn": "9780451524935"}'
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

