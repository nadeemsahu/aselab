#!/usr/bin/env python3
"""
Library Management System (LMS)
Core application handling books, members, borrowing/returning, and inventory management.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional


# Baseline System Policies (Configured on main)
DEFAULT_LOAN_DAYS: int = 14
DEFAULT_DAILY_FINE: float = 1.00
MAX_BORROW_LIMIT: int = 3


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    genre: str
    total_copies: int
    available_copies: int

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
        }


@dataclass
class Member:
    member_id: str
    name: str
    email: str
    borrowed_books: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": self.borrowed_books,
        }


@dataclass
class LoanRecord:
    record_id: str
    member_id: str
    book_id: str
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    fine_amount: float = 0.0


class Library:
    def __init__(self, name: str = "Central Library"):
        self.name: str = name
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.loans: List[LoanRecord] = []
        self._next_loan_id: int = 1

    def add_book(self, book_id: str, title: str, author: str, genre: str, copies: int = 1) -> Book:
        if book_id in self.books:
            existing = self.books[book_id]
            existing.total_copies += copies
            existing.available_copies += copies
            return existing
        book = Book(
            book_id=book_id,
            title=title,
            author=author,
            genre=genre,
            total_copies=copies,
            available_copies=copies,
        )
        self.books[book_id] = book
        return book

    def register_member(self, member_id: str, name: str, email: str) -> Member:
        if member_id in self.members:
            raise ValueError(f"Member ID {member_id} already registered.")
        member = Member(member_id=member_id, name=name, email=email)
        self.members[member_id] = member
        return member

    def get_book(self, book_id: str) -> Optional[Book]:
        return self.books.get(book_id)

    def get_member(self, member_id: str) -> Optional[Member]:
        return self.members.get(member_id)

    def borrow_book(self, member_id: str, book_id: str, loan_days: int = DEFAULT_LOAN_DAYS) -> LoanRecord:
        member = self.get_member(member_id)
        if not member:
            raise ValueError(f"Member '{member_id}' not found.")

        if len(member.borrowed_books) >= MAX_BORROW_LIMIT:
            raise ValueError(f"Member '{member_id}' reached borrow limit ({MAX_BORROW_LIMIT} books).")

        book = self.get_book(book_id)
        if not book:
            raise ValueError(f"Book '{book_id}' not found.")

        if book.available_copies <= 0:
            raise ValueError(f"Book '{book.title}' is currently out of stock.")

        now = datetime.now()
        due = now + timedelta(days=loan_days)
        loan = LoanRecord(
            record_id=f"LN-{self._next_loan_id:04d}",
            member_id=member_id,
            book_id=book_id,
            borrow_date=now,
            due_date=due,
        )
        self._next_loan_id += 1

        book.available_copies -= 1
        member.borrowed_books.append(book_id)
        self.loans.append(loan)
        return loan

    def calculate_fine(self, loan: LoanRecord, return_date: datetime, daily_rate: float = DEFAULT_DAILY_FINE) -> float:
        if return_date <= loan.due_date:
            return 0.0
        overdue_days = (return_date - loan.due_date).days
        return round(max(0, overdue_days * daily_rate), 2)

    def return_book(self, member_id: str, book_id: str, return_date: Optional[datetime] = None) -> float:
        member = self.get_member(member_id)
        if not member or book_id not in member.borrowed_books:
            raise ValueError(f"Member '{member_id}' has not borrowed book '{book_id}'.")

        active_loan = None
        for loan in reversed(self.loans):
            if loan.member_id == member_id and loan.book_id == book_id and loan.return_date is None:
                active_loan = loan
                break

        if not active_loan:
            raise ValueError(f"No active loan found for member '{member_id}' and book '{book_id}'.")

        actual_return = return_date or datetime.now()
        fine = self.calculate_fine(active_loan, actual_return)

        active_loan.return_date = actual_return
        active_loan.fine_amount = fine

        book = self.get_book(book_id)
        if book:
            book.available_copies += 1

        member.borrowed_books.remove(book_id)
        return fine

    def search_books(self, query: str, field: str = "title") -> List[Book]:
        """
        Search books by 'title', 'author', or 'genre'.
        Case-insensitive substring matching.
        """
        q = query.strip().lower()
        results: List[Book] = []
        for book in self.books.values():
            target_val = ""
            if field == "title":
                target_val = book.title.lower()
            elif field == "author":
                target_val = book.author.lower()
            elif field == "genre":
                target_val = book.genre.lower()
            else:
                target_val = f"{book.title} {book.author} {book.genre}".lower()

            if q in target_val:
                results.append(book)
        return results

    def list_inventory(self) -> List[dict]:
        return [b.to_dict() for b in self.books.values()]


def run_demo():
    print("=" * 60)
    print(" 📚 CENTRAL LIBRARY MANAGEMENT SYSTEM - DEMO")
    print("=" * 60)

    lib = Library("University Central Library")

    # Seed Books
    lib.add_book("B101", "Clean Code", "Robert C. Martin", "Software Engineering", 3)
    lib.add_book("B102", "Design Patterns", "Erich Gamma et al.", "Software Engineering", 2)
    lib.add_book("B103", "The Pragmatic Programmer", "Andy Hunt", "Software Engineering", 1)

    # Seed Members
    lib.register_member("M001", "Alice Johnson", "alice@university.edu")
    lib.register_member("M002", "Bob Smith", "bob@university.edu")

    print(f"\n[+] Library initialized with {len(lib.books)} books and {len(lib.members)} members.")

    # Borrow Book
    loan = lib.borrow_book("M001", "B101")
    print(f"[✓] Alice borrowed 'Clean Code' (Loan ID: {loan.record_id}, Due: {loan.due_date.strftime('%Y-%m-%d')})")
    print(f"    Available copies of B101: {lib.get_book('B101').available_copies}")

    # Return with Overdue simulation
    future_date = datetime.now() + timedelta(days=20)
    fine = lib.return_book("M001", "B101", return_date=future_date)
    print(f"[✓] Alice returned 'Clean Code' 6 days overdue. Fine assessed: ${fine:.2f}")
    print(f"    Available copies of B101: {lib.get_book('B101').available_copies}")

    print("\n[+] Inventory Summary:")
    for b in lib.list_inventory():
        print(f"    - [{b['book_id']}] {b['title']} by {b['author']} ({b['available_copies']}/{b['total_copies']} available)")

    print("=" * 60)


if __name__ == "__main__":
    run_demo()
