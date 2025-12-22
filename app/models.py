from pydantic import BaseModel, Field


class Book(BaseModel):
    """Canonical Book model used across the application."""

    isbn: str = Field(..., min_length=10, max_length=13)
    title: str
    author: str
    status: str = Field(default="available")

    def display_info(self) -> str:
        """Human-readable representation used by CLI and legacy code."""
        return f"'{self.title}' by {self.author}"


