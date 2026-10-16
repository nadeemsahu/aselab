#!/usr/bin/env python3
"""
Unit tests for the Library Management System.
"""

import unittest
from datetime import datetime, timedelta
from library import Library, DEFAULT_LOAN_DAYS, DEFAULT_DAILY_FINE, MAX_BORROW_LIMIT


class TestLibraryManagement(unittest.TestCase):
    def setUp(self):
        self.lib = Library("Test Library")
        self.lib.add_book("B01", "Refactoring", "Martin Fowler", "Tech", 2)
        self.lib.register_member("M01", "John Doe", "john@example.com")

    def test_add_and_get_book(self):
        book = self.lib.get_book("B01")
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Refactoring")
        self.assertEqual(book.total_copies, 2)
        self.assertEqual(book.available_copies, 2)

    def test_add_existing_book_increments_copies(self):
        self.lib.add_book("B01", "Refactoring", "Martin Fowler", "Tech", 3)
        book = self.lib.get_book("B01")
        self.assertEqual(book.total_copies, 5)
        self.assertEqual(book.available_copies, 5)

    def test_register_duplicate_member_raises_error(self):
        with self.assertRaises(ValueError):
            self.lib.register_member("M01", "John Duplicate", "john2@example.com")

    def test_borrow_book_success(self):
        loan = self.lib.borrow_book("M01", "B01")
        self.assertIsNotNone(loan)
        self.assertEqual(loan.member_id, "M01")
        self.assertEqual(loan.book_id, "B01")
        book = self.lib.get_book("B01")
        self.assertEqual(book.available_copies, 1)
        member = self.lib.get_member("M01")
        self.assertIn("B01", member.borrowed_books)

    def test_borrow_limit_exceeded(self):
        # Fill up to borrow limit
        for i in range(MAX_BORROW_LIMIT):
            bid = f"BLIM_{i}"
            self.lib.add_book(bid, f"Book {i}", "Author", "Genre", 5)
            self.lib.borrow_book("M01", bid)

        # Attempt to exceed limit
        self.lib.add_book("BLIM_EXC", "Over Limit Book", "Author", "Genre", 5)
        with self.assertRaises(ValueError) as ctx:
            self.lib.borrow_book("M01", "BLIM_EXC")
        self.assertIn("borrow limit", str(ctx.exception))

    def test_borrow_out_of_stock(self):
        self.lib.borrow_book("M01", "B01")
        self.lib.register_member("M02", "Jane Doe", "jane@example.com")
        self.lib.borrow_book("M02", "B01")

        self.lib.register_member("M03", "Jack", "jack@example.com")
        with self.assertRaises(ValueError) as ctx:
            self.lib.borrow_book("M03", "B01")
        self.assertIn("out of stock", str(ctx.exception))

    def test_return_book_on_time_no_fine(self):
        loan = self.lib.borrow_book("M01", "B01")
        on_time = loan.due_date - timedelta(days=2)
        fine = self.lib.return_book("M01", "B01", return_date=on_time)
        self.assertEqual(fine, 0.0)
        book = self.lib.get_book("B01")
        self.assertEqual(book.available_copies, 2)
        member = self.lib.get_member("M01")
        self.assertNotIn("B01", member.borrowed_books)

    def test_return_book_overdue_calculates_fine(self):
        loan = self.lib.borrow_book("M01", "B01")
        overdue_date = loan.due_date + timedelta(days=5)
        fine = self.lib.return_book("M01", "B01", return_date=overdue_date)
        self.assertEqual(fine, 5 * DEFAULT_DAILY_FINE)

    def test_inventory_listing(self):
        inv = self.lib.list_inventory()
        self.assertEqual(len(inv), 1)
        self.assertEqual(inv[0]["book_id"], "B01")

    def test_search_books_by_title_and_author(self):
        self.lib.add_book("B02", "Clean Architecture", "Robert C. Martin", "Architecture", 1)
        # By title
        title_matches = self.lib.search_books("Architecture", field="title")
        self.assertEqual(len(title_matches), 1)
        self.assertEqual(title_matches[0].book_id, "B02")

        # By author
        author_matches = self.lib.search_books("Martin", field="author")
        # Matches Fowler (Martin Fowler) and Martin (Robert C. Martin)
        self.assertEqual(len(author_matches), 2)

        # By genre
        genre_matches = self.lib.search_books("Tech", field="genre")
        self.assertEqual(len(genre_matches), 1)
        self.assertEqual(genre_matches[0].book_id, "B01")


if __name__ == "__main__":
    unittest.main()

