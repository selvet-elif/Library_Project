# Project Spec: Library System Refactor

## 1. Context & Role
**Role:** Senior Full-Stack Cloud Engineer
**Goal:** Transform the existing local Python script into a production-grade, cloud-native web application.
**Philosophy:** - **Declarative Code:** Prefer clean, readable abstractions over imperative "spaghetti" code.
- **Component-Based:** Both backend and frontend should be modular.
- **Strict Typing:** Use Pydantic and TypeScript interfaces for all data structures.

---

## 2. Global Constraints (The "Stack")

| Component | Technology Choice |
| :--- | :--- |
| **Language** | Python 3.10+ (Backend), TypeScript (Frontend) |
| **Framework** | FastAPI (API), React + Vite (UI) |
| **Styling** | Tailwind CSS |
| **Database** | AWS RDS PostgreSQL (via `asyncpg` + SQLModel) |
| **Infrastructure** | AWS (simulated or real credentials) |

---

## 3. Module Specifications

### Module A: Domain & API Layer
**Focus:** Code Quality, Asynchrony, and Separation of Concerns.

* **Unified Model:** * Create a canonical `Book` model in `app/models/`. 
    * *Constraint:* Ensure `library.py` and `openlibrary.py` both use this single model.
* **Service Layer Pattern:**
    * **Refactor:** `Library.add_book(book: Book)` must accept a domain object.
    * **Logic Flow:** `API Route` -> `OpenLibrary Client` -> `Book Model` -> `Library Service`.
* **Async Implementation:**
    * Convert `fetch_book_from_api` to `async def` using `httpx.AsyncClient`.
    * Ensure all FastAPI routes utilize `await`.

### Module B: Infrastructure & Persistence
**Focus:** Moving from JSON file storage to Cloud Database.

* **Database:** PostgreSQL on AWS RDS.
* **ORM:** SQLModel (SQLAlchemy wrapper).
* **Schema:**
    * `Book` (isbn, title, author, status)
    * `Member` (id, name, join_date)
    * `BorrowRecord` (member_id, isbn, borrow_date, return_date)
* **Configuration:**
    * Use `pydantic-settings`.
    * Load `POSTGRES_USER`, `POSTGRES_HOST`, etc., from `.env`.

### Module C: Frontend (SPA)
**Focus:** Modern, responsive UI consuming the API.

* **Setup:** `npm create vite@latest frontend -- --template react-ts`
* **Styling:** Install and configure Tailwind CSS.
* **Components:**
    * `<BookCard />`: Displays title, author, and status.
    * `<Dashboard />`: Grid layout of BookCards with pagination.
    * `<AddBookForm />`: Input for ISBN with validation and toast notifications.
* **Integration:**
    * Use `fetch` or `React Query` to communicate with the FastAPI backend.
    * Enable CORS in FastAPI for `localhost:5173`.

---

## 4. Implementation Steps (Execution Plan)

Please execute the refactoring in the following order. **Do not proceed to the next step until the current one is verified.**

1.  **Backend Core:**
    - [ ] Define the unified `Book` Pydantic model.
    - [ ] Make `OpenLibrary` client async.
    - [ ] Refactor `Library.add_book` to use the unified model.

2.  **Database Integration:**
    - [ ] Configure `SQLModel` connection to AWS RDS (or local Postgres fallback).
    - [ ] Create DB migrations/tables for Books, Members, and Borrowing.
    - [ ] Replace JSON file IO with DB Repository methods.

3.  **API Expansion:**
    - [ ] Create endpoints: `POST /members`, `POST /borrow`, `POST /return`.
    - [ ] Add filtering/pagination to `GET /books`.

4.  **Frontend Build:**
    - [ ] Initialize React + Tailwind project.
    - [ ] Build the Dashboard to list books from the API.
    - [ ] Build the "Add Book" flow.

---

## 5. Definition of Done
The project is considered complete when:
1.  Running `docker-compose up` (or equivalent) starts both Backend and Frontend.
2.  A user can add a book by ISBN via the UI, and it persists to the Postgres DB.
3.  A user can "borrow" a book, changing its status in the DB and UI.