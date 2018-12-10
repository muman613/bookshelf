import psycopg2 as pg
from bookshelf.book import Book
from enum import IntEnum


DB_NAME = "bookshelf"
USER_NAME = "bookshelf"
HOST_NAME = "laserquad.ddns.net"
PASSWD = "default"


class SortBy(IntEnum):
    """
    Enumerated type representing the sort order used to retreive the bookself.
    """
    ISBN = 1
    TITLE = 2
    PUBLISHER = 3
    AUTHOR = 4
    PUBDATE = 5
    PAGES = 6



class BookShelf:
    def __init__(self):
        self.db_conn = None

    def open(self):
        self.db_conn = pg.connect(dbname=DB_NAME, user=USER_NAME, password=PASSWD, host=HOST_NAME)
        return self.db_conn.status == pg.extensions.STATUS_READY

    def close(self):
        self.db_conn.close()

    def add_book(self, book: Book):
        with self.db_conn as connect:
            with connect.cursor() as cur:
                cmd = "INSERT INTO book_table(isbn, title, publisher, author, pub_date, pages, description, cover_image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
                cur.execute(cmd, (book.isbn, book.title, book.publisher, book.author, book.pubdate, book.pages, book.desc, book.image))

    def del_book(self, book: Book):
        with self.db_conn as connect:
            with connect.cursor() as cur:
                cmd = "DELETE FROM book_table WHERE isbn=%s;"
                cur.execute(cmd, (book.isbn, ))

    def update_book(self, book: Book):
        with self.db_conn as connect:
            with connect.cursor() as cur:
                cmd = """
                UPDATE book_table
                SET title = %s,
                    publisher = %s,
                    author = %s,
                    pub_date = %s,
                    pages = %s,
                    description = %s,
                    cover_image = %s
                WHERE
                    isbn=%s
                """

                cur.execute(cmd, (book.title, book.publisher, book.author, book.pubdate, book.pages, book.desc, book.image, book.isbn))


    def get_books_to_list(self, l: list, sortby=None):
        with self.db_conn as conn:
            with conn.cursor() as cur:
                by_field = "isbn"
                if sortby is not None:
                    book_fields = list(Book().get_keys())
                    by_field = book_fields[int(sortby) - 1]

                cmd = "SELECT * FROM book_table ORDER BY {}".format(by_field)
                cur.execute(cmd)
                rows = cur.fetchall()
                for row in rows:
                    book = Book()
                    book.isbn = row[0]
                    book.title = row[1]
                    book.publisher = row[2]
                    book.author = row[3]
                    book.pubdate = row[4]
                    book.pages = row[5]
                    book.desc = row[6]
                    book.image = row[7]
                    l.append(book)

        return True


def test():
    import time
    test_isbn = "9781571104052"

    bs = BookShelf()
    if bs.open():

        booklist = []

        bs.get_books_to_list(booklist)
        for which_book in booklist:
            print(which_book)

        print("=" * 128)
        book_obj = Book(test_isbn)
        print(book_obj)

        bs.add_book(book_obj)
        time.sleep(10) # Give user time to check that the database was altered
        bs.del_book(book_obj)

        bs.close()


def update_images(bs: BookShelf, to: int =5):
    import time
    index = 1;
    booklist = list()

    bs.get_books_to_list(booklist)

    for which_book in booklist:
        book_copy = Book(which_book.isbn)
        print("{} {}".format(index, book_copy))
        bs.update_book(book_copy)
        time.sleep(to)
        index += 1


def main():
    bs = BookShelf()
    if bs.open():
        booklist = []

        bs.get_books_to_list(booklist, sortby=SortBy.TITLE)
        print("The bookshelf contains {} books".format(len(booklist)))
        for key in Book().get_keys():
            print("Key: {}".format(key))


#        book_copy = Book(booklist[0].isbn)
 #       print(book_copy)
  #      bs.update_book(book_copy)

        bs.close()


# If the user ran this script run the main function
if __name__ == "__main__":
    main()
