#!/usr/bin/env python3

import unittest
from bookshelf.bookshelf import *


class BookTestCase(unittest.TestCase):
    """
    Tests for the Book class.
    """

    test_isbn_1 = "9781571104052"
    test_isbn_2 = "9780134034287"

    def test_google_api(self):
        """
        Test the retrieval of the book information from the Google API.
        """
        b = Book(self.test_isbn_1)
        self.assertTrue(b.isbn == self.test_isbn_1)
        self.assertTrue(b.title == "Teaching the Best Practice Way")

    def test_equality(self):
        """
        Test if two books are equal or not
        """
        b1 = Book(self.test_isbn_1)
        b2 = Book(self.test_isbn_2)
        self.assertTrue(b1 == b1)
        self.assertTrue(b2 == b2)
        self.assertTrue(b1 != b2)

    def test_attributes(self):
        """
        Test setting and getting book attributes.
        """
        title = "Uncle Johns Band"
        publisher = "Bill Graham Productions"
        pubdate = "1965"
        b = Book()
        b.isbn = self.test_isbn_1
        b.title = title
        b.publisher = publisher
        b.pubdate = pubdate

        self.assertTrue(b.isbn == self.test_isbn_1 and b.title == title and b.publisher == publisher and b.pubdate == pubdate)


class BookshelfTestCase(unittest.TestCase):
    """
    Tests for the bookshelf class.
    """

    test_isbn = "9781571104052"

    def test_store_delete(self):
        """
        Test the insertion and deletion of a book from the bookshelf storage.
        :return:
        """

        def add_book(bs: BookShelf, b: Book):
            try:
                bs.add_book(b)
                bs.get_books_to_list(book_list)

                self.assertTrue(b in book_list)

                bs.del_book(b)

                book_list.clear()
            except Exception as e:
                return False

            return True

        bs = BookShelf()
        if bs.open():
            book_list = []

            b = Book(self.test_isbn)

            self.assertFalse(add_book(bs, b), msg="Security warning, it seems that bookshelf_user can add!")

            bs.get_books_to_list(book_list)
            self.assertTrue(b not in book_list)


if __name__ == "__main__":
    unittest.main(verbosity=2)
