# Quick Start Guide

## Prerequisites

- Python 3.10+ with pip
- Node.js 18+ with npm
- PostgreSQL (local or Docker)

## Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL:**
   
   Option A: Using Docker (Recommended)
   ```bash
   docker run --name library-postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_DB=library_db \
     -p 5432:5432 \
     -d postgres:15
   ```
   
   Option B: Install PostgreSQL locally and create database `library_db`

3. **Create `.env` file:**
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=library_db
   ```

4. **Start the backend:**
   ```bash
   uvicorn api:app --reload
   ```
   
   Backend will be available at `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:5173`

## Usage

1. **Add a book:**
   - Enter an ISBN (10 or 13 digits) in the "Add New Book" form
   - Click "Add Book"
   - Book details will be fetched from OpenLibrary API

2. **View books:**
   - Books are displayed in a responsive grid
   - Use filters to search by author, title, or status
   - Use pagination to navigate through pages

3. **Delete a book:**
   - Click the delete icon on any book card
   - Confirm the deletion

## Testing the Full Stack

1. Start PostgreSQL (if using Docker):
   ```bash
   docker start library-postgres
   ```

2. Start the backend:
   ```bash
   uvicorn api:app --reload
   ```

3. Start the frontend (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

4. Open `http://localhost:5173` in your browser

5. Try adding a book with ISBN: `9780451524935` (1984 by George Orwell)

## Project Structure

```
Library_Project/
├── api.py                 # FastAPI application
├── app/                   # Backend application code
│   ├── models.py          # Domain models
│   ├── db_models.py       # Database models
│   ├── repositories.py    # Data access layer
│   ├── services.py        # Business logic
│   ├── database.py        # Database connection
│   └── config.py          # Configuration
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── api.ts        # API client
│   │   └── types.ts      # TypeScript types
│   └── package.json
└── requirements.txt       # Python dependencies
```

## Troubleshooting

### Backend Issues

- **Database connection error:** Make sure PostgreSQL is running and `.env` file is configured correctly
- **Port 8000 already in use:** Change the port in `api.py` or stop the process using port 8000

### Frontend Issues

- **CORS errors:** Make sure backend CORS is configured for `localhost:5173`
- **API connection failed:** Verify backend is running on `http://localhost:8000`
- **Build errors:** Run `npm install` again to ensure all dependencies are installed

## Production Build

### Backend
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
# Serve the dist/ directory with a web server
```

## Next Steps

- Add user authentication
- Add borrow/return UI
- Add member management UI
- Deploy to cloud (AWS, Vercel, etc.)

