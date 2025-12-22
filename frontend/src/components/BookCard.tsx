import type { Book } from "../types";

interface BookCardProps {
  book: Book;
  onDelete?: (isbn: string) => void;
}

export function BookCard({ book, onDelete }: BookCardProps) {
  const statusColors = {
    available: "bg-green-100 text-green-800 border-green-300",
    borrowed: "bg-red-100 text-red-800 border-red-300",
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">{book.title}</h3>
          <p className="text-gray-600 mb-3">by {book.author}</p>
          <div className="flex items-center gap-2">
            <span
              className={`px-3 py-1 rounded-full text-xs font-medium border ${statusColors[book.status]}`}
            >
              {book.status === "available" ? "Available" : "Borrowed"}
            </span>
            <span className="text-xs text-gray-500">ISBN: {book.isbn}</span>
          </div>
        </div>
        {onDelete && (
          <button
            onClick={() => onDelete(book.isbn)}
            className="ml-4 text-red-600 hover:text-red-800 transition-colors"
            aria-label="Delete book"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}

