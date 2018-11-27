import psycopg2 as pg
from book import Book


DB_NAME = "bookshelf"
USER_NAME = "bookshelf"
HOST_NAME = "raspi-mate"
PASSWD = "default"


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
                cmd = "INSERT INTO book_table(isbn, title, publisher, author, pub_date, pages, description) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                cur.execute(cmd, (book.isbn, book.title, book.publisher, book.author, book.pubdate, book.pages, book.desc))

    def del_book(self, book: Book):
        with self.db_conn as connect:
            with connect.cursor() as cur:
                cmd = "DELETE FROM book_table WHERE isbn=%s;"
                cur.execute(cmd, (book.isbn, ))

    def get_books_to_list(self, l: list):
        with self.db_conn as conn:
            with conn.cursor() as cur:
                cmd = "SELECT * FROM book_table ORDER BY isbn;"
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


def main():
    bs = BookShelf()
    if bs.open():
        booklist = []

        bs.get_books_to_list(booklist)
        print("The bookshelf contains {} books".format(len(booklist)))
        for which_book in booklist:
            print(which_book)

        bs.close()


# If the user ran this script run the main function
if __name__ == "__main__":
    main()
