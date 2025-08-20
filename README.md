# Library_Project
# Library Management API

A simple Library Management example project that includes a FastAPI-based REST API, a small library model, and tests for OpenLibrary integration.

## Repository contents

- `api.py` — FastAPI application exposing endpoints to add/list/delete books, and a health check.
- `library.py` — Core library models and a `Library` class with JSON-backed persistence utilities.
- `test_openlibrary.py` — Pytest tests for the `fetch_book_from_api` behavior (uses mocking of `httpx.get`).

> Note: This README assumes the code in the repository is used as-is. There are a few small issues in the current code base that are explained in **Notes & required fixes** below.

---

## Quick features

- Add a book by ISBN (calls OpenLibrary to fetch metadata).
- List stored books (JSON file persistence).
- Delete a book by ISBN.
- Health endpoint with a quick status and stored book count.
- Unit tests that mock external HTTP calls.

---

## Requirements

You can create a `requirements.txt` with at least the following packages:

```
fastapi
uvicorn
pydantic
httpx
pytest
```

Install via:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install fastapi uvicorn httpx pytest
```

---

## Installation & Local run

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate    # Windows
```

2. Install requirements (see above).

3. Run the API using Uvicorn:

```bash
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`. OpenAPI docs: `http://127.0.0.1:8000/docs`.

---

## API Endpoints (summary)

- `GET /` — Welcome message.
- `GET /books` — Get all stored books (JSON list).
- `POST /books` — Add a book by providing JSON `{"isbn": "<ISBN>"}`. The endpoint fetches metadata from OpenLibrary and stores it.
- `GET /books/{isbn}` — Retrieve a single book by ISBN.
- `DELETE /books/{isbn}` — Delete a book by ISBN.
- `GET /health` — Returns a simple health payload and the stored book count.

Refer to the FastAPI OpenAPI UI at `/docs` for details and example payloads.

---

## Running tests

The repository includes `test_openlibrary.py` which uses `pytest` and mocks `httpx.get` calls. Run tests with:

## Contribution

1. Fork the repository.
2. Create a branch for your changes.
3. Implement `openlibrary.py` (or convert to an async flow) and fix the `library.py` usage examples.
4. Add or update tests as needed.
5. Create a Pull Request describing the changes.

---

---

