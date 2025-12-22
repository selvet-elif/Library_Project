import { useState, useEffect } from "react";
import { BookCard } from "./BookCard";
import { fetchBooks, deleteBook } from "../api";
import type { Book } from "../types";
import toast from "react-hot-toast";

const ITEMS_PER_PAGE = 12;

export function Dashboard() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(0);
  const [total, setTotal] = useState(0);
  const [filters, setFilters] = useState<{
    author?: string;
    title?: string;
    status?: string;
  }>({});

  const loadBooks = async () => {
    setLoading(true);
    try {
      const skip = currentPage * ITEMS_PER_PAGE;
      const response = await fetchBooks(skip, ITEMS_PER_PAGE, filters);
      setBooks(response.items);
      setTotal(response.total);
    } catch (error) {
      toast.error("Failed to load books");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBooks();
  }, [currentPage, filters]);

  const handleDelete = async (isbn: string) => {
    if (!confirm("Are you sure you want to delete this book?")) {
      return;
    }

    try {
      await deleteBook(isbn);
      toast.success("Book deleted successfully");
      loadBooks();
    } catch (error) {
      toast.error("Failed to delete book");
      console.error(error);
    }
  };

  const handleFilterChange = (key: "author" | "title" | "status", value: string) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value || undefined,
    }));
    setCurrentPage(0); // Reset to first page when filter changes
  };

  const totalPages = Math.ceil(total / ITEMS_PER_PAGE);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">Library Dashboard</h1>

          {/* Filters */}
          <div className="bg-white rounded-lg shadow-md p-4 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Filter by Author
                </label>
                <input
                  type="text"
                  value={filters.author || ""}
                  onChange={(e) => handleFilterChange("author", e.target.value)}
                  placeholder="Search by author..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Filter by Title
                </label>
                <input
                  type="text"
                  value={filters.title || ""}
                  onChange={(e) => handleFilterChange("title", e.target.value)}
                  placeholder="Search by title..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Filter by Status
                </label>
                <select
                  value={filters.status || ""}
                  onChange={(e) => handleFilterChange("status", e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                >
                  <option value="">All</option>
                  <option value="available">Available</option>
                  <option value="borrowed">Borrowed</option>
                </select>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="mb-4 text-gray-600">
            Showing {books.length} of {total} books
          </div>
        </div>

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : books.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No books found.</p>
            <p className="text-gray-400 text-sm mt-2">
              Try adjusting your filters or add a new book.
            </p>
          </div>
        ) : (
          <>
            {/* Book Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
              {books.map((book) => (
                <BookCard key={book.isbn} book={book} onDelete={handleDelete} />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center gap-2">
                <button
                  onClick={() => setCurrentPage((p) => Math.max(0, p - 1))}
                  disabled={currentPage === 0}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Previous
                </button>
                <span className="px-4 py-2 text-gray-700">
                  Page {currentPage + 1} of {totalPages}
                </span>
                <button
                  onClick={() => setCurrentPage((p) => Math.min(totalPages - 1, p + 1))}
                  disabled={currentPage >= totalPages - 1}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

