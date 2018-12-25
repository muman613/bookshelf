import curses
import psycopg2 as pg
from bookshelf.book import Book


class BookScanner:
    """
    This class encapsulates the book scanning application. This app has a curses text user interface which
    basically waits for the user to scan in the ISBN barcodes and then looks up the ISBN on the google book API url.
    """

    DB_NAME = "bookshelf"
    USER_NAME = "bookshelf"
    HOST_NAME = "raspi-mate"
    PASSWD = "default"

    def __init__(self, scr):
        self.last_scanned_code = None
        self.book_list = []
        self.width = 0
        self.height = 0
        self.scr = scr
        self.height, self.width = scr.getmaxyx()

        BookScanner.init_color_pairs()

        # sw = scr.subwin(self.height - 20, self.width - 20, 10, 10)
        # sw.bkgd(" ", curses.color_pair(2))
        # sw.border()
        # self.sw = sw
        self.bookwin = None
        self.statwin = None
        self.create_subwindows()
        # curses.nonl()
        curses.curs_set(0)
        self.scr.nodelay(True)
        self.scr.border()
        self.conn = None

        self.open_database()
        self.load_books_from_db()

#       atexit.register(self.close_database)

    # def __del__(self):
    #     self.close_database()

    def create_subwindows(self):
        bookwin_h = 12

        sw = self.scr.subwin(bookwin_h, self.width - 20, 10, 10)
        sw.bkgd(" ", curses.color_pair(2))
        sw.border()
        self.bookwin = sw

        statwin_h = 8
        sw = self.scr.subwin(statwin_h, self.width - 20, 24, 10)
        sw.bkgd(" ", curses.color_pair(3))
        sw.border()
        self.statwin = sw

    def open_database(self):
        self.conn = pg.connect(database=self.DB_NAME, user=self.USER_NAME, password=self.PASSWD, host=self.HOST_NAME)

    def close_database(self):
        if self.conn:
            self.conn.close()

    def load_books_from_db(self):
        """
        Load all the books in the bookshelf into the list
        :return:
        """
        with self.conn as conn:
            with conn.cursor() as curs:
                cmd = "SELECT * FROM book_table ORDER BY isbn;"
                curs.execute(cmd)
                rows = curs.fetchall()
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

                    self.book_list.append(book)

    def add_book_to_db(self, book: Book):
        """
        Add the scanned book to the database

        TODO: Use the bookshelf class to handle insertion of new book.

        :param book: book object representing the new record
        :return:
        """
        try:
            with self.conn as connect:
                with connect.cursor() as cur:
                    cmd = "INSERT INTO book_table(isbn, title, publisher, author, pub_date, pages, description, cover_image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
                    cur.execute(cmd, (book.isbn, book.title, book.publisher, book.author, book.pubdate, book.pages, book.desc, book.image))
        except psycopg2.Error as e:
            pass

    def draw_book(self, book: Book):
        def add_label(y, label_text, field, dflt="N/A", use_value=None):
            value = None
            if use_value is None and book:
                value = str(book[field]) if hasattr(book, field) else "N/A"
            else:
                value = use_value

            field_label = "{:12} : {:60}".format(label_text, value)
            self.bookwin.addstr(y, 10, field_label)

        self.bookwin.clear()
        self.bookwin.border()

        startrow = 2

        add_label(startrow, "Title", "title")
        startrow += 1

        add_label(startrow, "Publisher", "publisher")
        startrow += 1

        add_label(startrow, "Author(s)", "author")
        startrow += 1

        add_label(startrow, "Published", "pubdate")
        startrow += 1

        add_label(startrow, "Pages", "pages")
        startrow += 1

    def center_label(self, scr, y: int, label: str, pair: int= 0):
        """
        Display label centered horizontally on the line
        :param scr: Window to write label to
        :param y: row to display label on
        :param label: text to display
        :param pair: color-pair to use
        """
        h, w = scr.getmaxyx()
        scr.addstr(y, int((w - len(label)) / 2), label, curses.color_pair(pair))

    def redraw_stats_subwin(self):
        self.statwin.clear()
        self.statwin.bkgd(" ", curses.color_pair(3))
        self.statwin.border()
        label = "Books on Shelf : {}".format(len(self.book_list))
        self.statwin.addstr(2, 10, label)

    def redraw_border(self):
        self.scr.border()
        self.center_label(self.scr, 0, "Book Scanning Application", 1)
        self.center_label(self.scr, 1, "By Michael Uman", 1)
        self.center_label(self.scr, self.height - 2, "Hit 'q' to exit")

    def display_product_rescan(self):
        """
        Display message indicating that the product has already been scanned.
        """
        self.bookwin.clear()
        self.bookwin.border()
        self.center_label(self.bookwin, 2, "<< Product Code Already Scanned >>", 3)

    def display_not_isbn_no(self):
        """
        Display message indicating the the product scanned was not a valid ISBN #
        """
        self.bookwin.clear()
        self.bookwin.border()
        self.center_label(self.bookwin, 2, "<< Not an ISBN code >>", 3)

    def is_isbn_in_list(self, isbn: str):
        for b in self.book_list:
            if b.isbn == isbn:
                return True
        return False

    def handle_scanned_code(self, isbn: str):
        if self.is_isbn_in_list(isbn):
            self.display_product_rescan()
        else:
            label = "Last ISBN # Scanned : {:14}".format(isbn)
            self.center_label(self.scr, 6, label)

            book = Book(isbn)
            if book:
                self.draw_book(book)
                self.add_book_to_db(book)
                self.book_list.append(book)
                self.last_scanned_code = isbn
            else:
                self.display_not_isbn_no()

        self.redraw_border()
        self.redraw_stats_subwin()

    def run(self):
        isbn_text = ""

        self.redraw_border()
        self.redraw_stats_subwin()

        while True:
            self.scr.refresh()

            s = self.scr.getch()
            if s != -1:
                if s == ord("q"):
                    break
                elif ord("0") <= s <= ord("9"):
                    isbn_text += chr(s)
                elif s == ord("\n"):
                    if isbn_text:
                        self.handle_scanned_code(isbn_text)
                    isbn_text = ""

    @staticmethod
    def init_color_pairs():
        """
        Initialize curses color pairs.
        :return:
        """
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_RED)


def bookshelf_main(stdscr):
    scanner = BookScanner(stdscr)
    scanner.run()


def main():
    curses.wrapper(bookshelf_main)


if __name__ == "__main__":
    main()
