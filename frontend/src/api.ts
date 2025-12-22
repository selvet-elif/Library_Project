/** API client for FastAPI backend */

const API_BASE_URL = "http://localhost:8000";

export async function fetchBooks(
  skip: number = 0,
  limit: number = 100,
  filters?: { author?: string; title?: string; status?: string }
): Promise<import("./types").PaginatedBookResponse> {
  const params = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString(),
  });

  if (filters?.author) params.append("author", filters.author);
  if (filters?.title) params.append("title", filters.title);
  if (filters?.status) params.append("status", filters.status);

  const response = await fetch(`${API_BASE_URL}/books?${params}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch books: ${response.statusText}`);
  }
  return response.json();
}

export async function addBook(isbn: string): Promise<import("./types").BookResponse> {
  const response = await fetch(`${API_BASE_URL}/books`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ isbn }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || `Failed to add book: ${response.statusText}`);
  }

  return response.json();
}

export async function deleteBook(isbn: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/books/${isbn}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Failed to delete book: ${response.statusText}`);
  }
}

