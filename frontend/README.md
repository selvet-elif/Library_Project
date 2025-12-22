# Library Management Frontend

Modern React + TypeScript frontend for the Library Management System.

## Features

- 📚 **Book Dashboard** - View all books in a responsive grid layout
- ➕ **Add Books** - Add books by ISBN with validation
- 🔍 **Filtering** - Filter books by author, title, or status
- 📄 **Pagination** - Navigate through large book collections
- 🎨 **Modern UI** - Built with Tailwind CSS
- 🔔 **Toast Notifications** - User-friendly feedback with react-hot-toast

## Tech Stack

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **react-hot-toast** - Toast notifications

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── BookCard.tsx      # Book card component
│   │   ├── Dashboard.tsx     # Main dashboard with grid and filters
│   │   └── AddBookForm.tsx   # Form to add books by ISBN
│   ├── api.ts                # API client functions
│   ├── types.ts              # TypeScript type definitions
│   ├── App.tsx               # Main app component
│   └── main.tsx              # Entry point
├── tailwind.config.js        # Tailwind configuration
└── postcss.config.js         # PostCSS configuration
```

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`. Make sure:

1. The backend is running
2. CORS is enabled (already configured in `api.py`)
3. Database is set up and initialized

## Components

### BookCard
Displays book information including title, author, ISBN, and status. Includes delete functionality.

### Dashboard
Main component that:
- Displays books in a responsive grid
- Provides filtering by author, title, and status
- Implements pagination
- Shows loading states and empty states

### AddBookForm
Form component that:
- Validates ISBN input (10 or 13 digits)
- Fetches book details from OpenLibrary API via backend
- Shows success/error toast notifications
- Refreshes the dashboard after adding a book

## Development

### Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

Currently, the API base URL is hardcoded in `src/api.ts`. To use a different backend URL, modify:

```typescript
const API_BASE_URL = "http://localhost:8000";
```

For production, consider using environment variables with Vite:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

Then create a `.env` file:
```
VITE_API_URL=http://your-backend-url.com
```
