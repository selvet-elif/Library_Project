# Library Project

A complete library management application, featuring a FastAPI backend and a React + TypeScript frontend, is provided in this repository. This project was developed to be straightforward, easily extensible, and simple to run locally. An overview of the project structure and setup instructions is included below.

**What's included**
- **Backend**: FastAPI app (entry: `api.py`) with endpoints to add, list, fetch and delete books, plus health and system endpoints.
- **Database layer**: SQLModel + PostgreSQL integration under `app/` with models, repositories and services.
- **Frontend**: A small React + TypeScript app in `frontend/` that can add books (by ISBN) and browse the library.
.

## What it does (brief)
- Book metadata is fetched from OpenLibrary when adding by ISBN.
- Books are stored in a PostgreSQL database using SQLModel.
- A JSON REST API is served and consumed by a Vite + React frontend.
- Basic tests are included, some of which mock external HTTP calls so they are run offline.

## Tech stack
- Python 3.10+, FastAPI, SQLModel (SQLAlchemy under the hood)
- PostgreSQL (local or Docker)
- Frontend: React + TypeScript, Vite
- Tests: pytest

## Getting started (quick)

The minimal steps to be followed to run both backend and frontend on your machine are presented below.

1) Install Python dependencies

```bash
pip install -r requirements.txt
```

2) Start a PostgreSQL instance

Option A — Docker (recommended):

```powershell
docker run --name library-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library_db -p 5432:5432 -d postgres:15
```

Option B — Local PostgreSQL: a database named `library_db` should be created and credentials should be ensured to match your `.env`.

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
- Add a book: an ISBN (10 or 13 digits) should be pasted into the frontend "Add Book" form. OpenLibrary will be queried by the backend for metadata, then the book will be stored.
- Browse books: the UI filters should be used to search by author, title or status.
- Delete: a book should be removed from the library via the UI (or the API).

## Important API endpoints (examples)
- `GET /books` — list books (supports pagination and filters)
- `POST /books` — add a book by sending `{ "isbn": "9780451524935" }`
- `GET /books/{isbn}` — get details for an ISBN
- `DELETE /books/{isbn}` — delete a book
- `GET /health` — health check and book count

For a complete reference, see [info/API_ENDPOINTS.md](info/API_ENDPOINTS.md).

## Tests
The test suite may be run with:

```bash
pytest -q
```

OpenLibrary is mocked by some tests so network access is not required. If tests that hit real services are to be run, network connectivity should be ensured.

## Development notes
- The backend code is located in `app/` — `models.py`, `db_models.py`, `repositories.py`, `services.py` and `database.py` are intentionally kept separated for clarity.
- Database tables are created automatically on app startup by the `init_db()` logic.
- Frontend API calls are found in `frontend/src/api.ts` and components are found in `frontend/src/components`.

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
- API docs: [info/API_ENDPOINTS.md]
- Run instructions & troubleshooting: [info/HOW_TO_RUN.md] and [info/QUICK_START.md]
- Database guide: [info/README_DATABASE.md]
- Frontend notes: [frontend/README_FRONTEND.md]






