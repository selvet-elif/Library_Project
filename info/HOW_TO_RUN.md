# How to Run the Library Management System

## Quick Start (Step-by-Step)

### Step 1: Set Up Database

**Option A: Using Docker (Easiest)**

Open PowerShell or Command Prompt and run:

```powershell
docker run --name library-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=library_db -p 5432:5432 -d postgres:15
```

**Option B: Install PostgreSQL Locally**

1. Download and install PostgreSQL from https://www.postgresql.org/download/
2. Create a database named `library_db`

### Step 2: Create Environment File

Create a file named `.env` in the project root (`C:\Users\selve\Documents\GitHub\Library_Project\.env`) with this content:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=library_db
```

### Step 3: Install Backend Dependencies

Open a terminal in the project root and run:

```powershell
pip install -r requirements.txt
```

### Step 4: Start the Backend Server

In the same terminal, run:

```powershell
uvicorn api:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
```

✅ Backend is now running at `http://localhost:8000`
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Step 5: Install Frontend Dependencies

Open a **NEW terminal window** and navigate to the frontend folder:

```powershell
cd frontend
npm install
```

### Step 6: Start the Frontend Server

In the frontend terminal, run:

```powershell
npm run dev
```

You should see:
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network:  use --host to expose
```

✅ Frontend is now running at `http://localhost:5173`

### Step 7: Open the Application

Open your browser and go to: **http://localhost:5173**

## What You'll See

1. **Add Book Form** at the top - Enter an ISBN to add a book
2. **Filters** - Search by author, title, or status
3. **Book Grid** - All books displayed in cards
4. **Pagination** - Navigate through pages if you have many books

## Try It Out!

1. **Add a book:** Enter ISBN `9780451524935` (1984 by George Orwell) and click "Add Book"
2. **Filter books:** Try searching by author "Orwell" or title "1984"
3. **Delete a book:** Click the trash icon on any book card

## Running Both Servers

You need **TWO terminal windows**:

**Terminal 1 (Backend):**
```powershell
# In project root
uvicorn api:app --reload
```

**Terminal 2 (Frontend):**
```powershell
# In frontend folder
cd frontend
npm run dev
```

## Stopping the Servers

- **Backend:** Press `Ctrl+C` in the backend terminal
- **Frontend:** Press `Ctrl+C` in the frontend terminal
- **Database:** If using Docker, run `docker stop library-postgres`

## Troubleshooting

### "Module not found" errors
```powershell
pip install -r requirements.txt
```

### "Port 8000 already in use"
- Find and stop the process using port 8000, or
- Change the port in `api.py` (line 194)

### "Cannot connect to database"
- Make sure PostgreSQL is running: `docker ps` (should show library-postgres)
- Check your `.env` file exists and has correct values
- Try restarting PostgreSQL: `docker restart library-postgres`

### Frontend shows "Failed to fetch"
- Make sure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify backend CORS is enabled (it should be)

### Frontend build errors
```powershell
cd frontend
npm install
npm run dev
```

## Quick Commands Reference

```powershell
# Start PostgreSQL (Docker)
docker start library-postgres

# Start Backend
uvicorn api:app --reload

# Start Frontend (in frontend/ directory)
npm run dev

# Stop PostgreSQL (Docker)
docker stop library-postgres
```

## Need Help?

- Check `QUICK_START.md` for more details
- Check `README_DATABASE.md` for database setup
- Check API docs at http://localhost:8000/docs when backend is running

