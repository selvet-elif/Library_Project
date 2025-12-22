/** TypeScript interfaces for API types */

export interface Book {
  isbn: string;
  title: string;
  author: string;
  status: "available" | "borrowed";
}

export interface BookResponse extends Book {}

export interface PaginatedBookResponse {
  items: BookResponse[];
  total: number;
  skip: number;
  limit: number;
}

export interface Member {
  id: number;
  name: string;
}

export interface BorrowRecord {
  id: number;
  member_id: number;
  isbn: string;
  borrow_date: string;
  return_date: string | null;
}

