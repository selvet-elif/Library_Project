# Library Project

Concise developer README for the Library Management example (backend + frontend).

## What it is

- FastAPI backend (API entry: `api.py`) providing book add/list/delete and health endpoints.
- React + TypeScript frontend in `frontend/` (Vite) for browsing and adding books.

## Quick start — Backend

1. (Optional) Create a venv and activate it.
2. Install Python deps:

```bash
pip install -r requirements.txt
```

3. Start the API in project root:

```bash
uvicorn api:app --reload
```

OpenAPI docs: `http://127.0.0.1:8000/docs`.

## Quick start — Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend dev server (default): `http://localhost:5173`.

## Essential API endpoints

- `GET /books` — list books
- `POST /books` — add a book (JSON: `{"isbn": "..."}`)
- `GET /books/{isbn}` — book details
- `DELETE /books/{isbn}` — remove a book
- `GET /health` — health + book count

## Tests

Run tests with:

```bash
pytest -q
```

Some tests mock OpenLibrary HTTP calls and do not require network access.

## Where to look next

- API endpoints docs: `info/API_ENDPOINTS.md`
- Run details: `info/QUICK_START.md` and `info/HOW_TO_RUN.md`
- Database info: `info/README_DATABASE.md`
- Frontend info: `README_FRONTEND.md`
---



