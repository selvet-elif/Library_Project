# Database Setup Guide

This project uses PostgreSQL with SQLModel for database operations.

## Prerequisites

1. **PostgreSQL** installed locally or access to AWS RDS PostgreSQL
2. Python dependencies installed: `pip install -r requirements.txt`

## Local PostgreSQL Setup

### Option 1: Using Docker (Recommended)

```bash
docker run --name library-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=library_db \
  -p 5432:5432 \
  -d postgres:15
```

### Option 2: Install PostgreSQL Locally

1. Install PostgreSQL from https://www.postgresql.org/download/
2. Create database:
   ```sql
   CREATE DATABASE library_db;
   ```

## Configuration

1. Create a `.env` file in the project root:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=library_db
   ```

2. For AWS RDS, update `.env`:
   ```env
   POSTGRES_HOST=your-rds-endpoint.region.rds.amazonaws.com
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_PORT=5432
   POSTGRES_DB=library_db
   ```

## Database Initialization

The database tables are automatically created when you start the FastAPI application. The `init_db()` function in `app/database.py` creates all tables defined in `app/db_models.py`.

## Database Schema

- **books**: Stores book information (isbn, title, author, status)
- **members**: Stores library members (id, name, join_date)
- **borrow_records**: Tracks book borrowing (member_id, isbn, borrow_date, return_date)

## Running the Application

```bash
# Start the API server
uvicorn api:app --reload

# The database tables will be created automatically on startup
```

## Testing Database Connection

You can test the database connection by:

1. Starting the API: `uvicorn api:app --reload`
2. Visiting `http://localhost:8000/docs` to see the API documentation
3. Testing endpoints like `GET /books` or `POST /books`

