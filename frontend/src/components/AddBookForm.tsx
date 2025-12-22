import { useState } from "react";
import { addBook } from "../api";
import toast from "react-hot-toast";

interface AddBookFormProps {
  onBookAdded: () => void;
}

export function AddBookForm({ onBookAdded }: AddBookFormProps) {
  const [isbn, setIsbn] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const validateISBN = (value: string): boolean => {
    // Remove hyphens and spaces
    const cleaned = value.replace(/[-\s]/g, "");
    // Check if it's 10 or 13 digits
    return /^\d{10}$|^\d{13}$/.test(cleaned);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clean ISBN (remove hyphens and spaces)
    const cleanedISBN = isbn.replace(/[-\s]/g, "");

    if (!validateISBN(cleanedISBN)) {
      toast.error("Please enter a valid ISBN (10 or 13 digits)");
      return;
    }

    setIsLoading(true);
    try {
      await addBook(cleanedISBN);
      toast.success("Book added successfully!");
      setIsbn("");
      onBookAdded();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to add book";
      toast.error(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Add New Book</h2>
      <div className="flex gap-4">
        <input
          type="text"
          value={isbn}
          onChange={(e) => setIsbn(e.target.value)}
          placeholder="Enter ISBN (10 or 13 digits)"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !isbn.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {isLoading ? "Adding..." : "Add Book"}
        </button>
      </div>
      <p className="text-sm text-gray-500 mt-2">
        Enter a valid ISBN number. The book details will be fetched from OpenLibrary.
      </p>
    </form>
  );
}

