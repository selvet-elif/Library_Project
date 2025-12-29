# Library Project

Welcome — this repository contains a small, complete example of a library management application: a FastAPI backend that stores books and a simple React + TypeScript frontend (Vite) that talks to it.

I developed this project to be easy to run locally, easy to extend, and straightforward to read. Below you'll find a human-friendly tour: what it does, how it is organized, and how to get it running for development or testing.

**What's included**
- **Backend**: FastAPI app (entry: `api.py`) with endpoints to add, list, fetch and delete books, plus health and system endpoints.
- **Database layer**: SQLModel + PostgreSQL integration under `app/` with models, repositories and services.
- **Frontend**: A small React + TypeScript app in `frontend/` that can add books (by ISBN) and browse the library.

Why you'll like it: the codebase is intentionally compact and idiomatic so it's a good starting point for experiments (authentication, borrowing flows, deployment, etc.).

## What it does (brief)
- Fetches book metadata from OpenLibrary when adding by ISBN.
- Stores books in a PostgreSQL database using SQLModel.
- Serves a JSON REST API consumed by a Vite + React frontend.
- Includes basic tests, some of which mock external HTTP calls so they run offline.

## Tech stack
- Python 3.10+, FastAPI, SQLModel (SQLAlchemy under the hood)
- PostgreSQL (local or Docker)
- Frontend: React + TypeScript, Vite
- Tests: pytest

## Getting started (quick)

These are the minimal steps to run both backend and frontend on your machine.

1) Install Python dependencies

```bash
pip install -r requirements.txt
```

2) Start a PostgreSQL instance

Option A — Docker (recommended):

```powershell
docker run --name library-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library_db -p 5432:5432 -d postgres:15
```

Option B — Local PostgreSQL: create a database named `library_db` and ensure credentials match your `.env`.

3) Create a `.env` file in the project root with these values (example):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=library_db
```

4) Start the backend (from project root)

```powershell
uvicorn api:app --reload
```

OpenAPI docs: http://127.0.0.1:8000/docs

5) Start the frontend (in a new terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend default URL: http://localhost:5173

## How to use the app (simple flows)
- Add a book: paste an ISBN (10 or 13 digits) into the frontend "Add Book" form. The backend will query OpenLibrary for metadata, then store the book.
- Browse books: use the UI filters to search by author, title or status.
- Delete: remove a book from the library via the UI (or the API).

## Important API endpoints (examples)
- `GET /books` — list books (supports pagination and filters)
- `POST /books` — add a book by sending `{ "isbn": "9780451524935" }`
- `GET /books/{isbn}` — get details for an ISBN
- `DELETE /books/{isbn}` — delete a book
- `GET /health` — health check and book count

For a complete reference, see [info/API_ENDPOINTS.md](info/API_ENDPOINTS.md).

## Tests
Run the test suite with:

```bash
pytest -q
```

Some tests mock OpenLibrary so they don't require network access. If you want to run tests that hit real services, make sure you have network connectivity.

## Development notes
- The backend code lives in `app/` — `models.py`, `db_models.py`, `repositories.py`, `services.py` and `database.py` are intentionally separated for clarity.
- Database tables are created automatically on app startup by the `init_db()` logic.
- Frontend API calls are in `frontend/src/api.ts` and components are in `frontend/src/components`.

## Useful commands

Start backend (project root):

```powershell
uvicorn api:app --reload
```

Start frontend (frontend folder):

```bash
cd frontend
npm run dev
```

Run tests:

```bash
pytest -q
```

## Next steps / ideas
- Add member management and borrowing flows to the frontend.
- Add authentication (JWT) to the API.
- Add CI (GitHub Actions) to run tests on PRs.

## Where to read more in this repo
- API docs: [info/API_ENDPOINTS.md](info/API_ENDPOINTS.md)
- Run instructions & troubleshooting: [info/HOW_TO_RUN.md](info/HOW_TO_RUN.md) and [info/QUICK_START.md](info/QUICK_START.md)
- Database guide: [info/README_DATABASE.md](info/README_DATABASE.md)
- Frontend notes: [frontend/README_FRONTEND.md](frontend/README_FRONTEND.md)

If you'd like I can tailor this README to be even more beginner-friendly (add screenshots, curl examples, or a short video-style walkthrough). Want me to add any of those?




