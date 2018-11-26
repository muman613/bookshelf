import curses
import json
import urllib.request

from book import Book


class BookScanner:
    """
    This class encapsulates the book scanning application. This app has a curses text user interface which
    basically waits for the user to scan in the ISBN barcodes and then looks up the ISBN on the google book API url.
    """

    def __init__(self, scr):
        self.last_scanned_code = None
        self.book_list = []
        self.width = 0
        self.height = 0
        self.scr = scr
        self.height, self.width = scr.getmaxyx()

        self.init_color_pairs()

        sw = scr.subwin(self.height - 20, self.width - 20, 10, 10)
        sw.bkgd(" ", curses.color_pair(2))
        sw.border()
        self.sw = sw
        # curses.nonl()
        curses.curs_set(0)
        self.scr.nodelay(True)
        self.scr.border()

    def draw_book(self, book: Book):
        def add_label(y, label_text, field, dflt="N/A", use_value=None):
            value = None
            if use_value is None and book:
                value = str(book[field]) if hasattr(book, field) else "N/A"
            else:
                value = use_value

            field_label = "{:12} : {:60}".format(label_text, value)
            self.sw.addstr(y, 10, field_label)

        self.sw.clear()
        self.sw.border()

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

    def redraw_border(self, scr):
        self.scr.border()
        self.center_label(self.scr, 0, "Book Scanning Application", 1)
        self.center_label(self.scr, 1, "By Michael Uman", 1)
        self.center_label(self.scr, self.height - 2, "Hit 'q' to exit")

    def display_product_rescan(self):
        """
        Display message indicating that the product has already been scanned.
        """
        self.sw.clear()
        self.sw.border()
        self.center_label(self.sw, 2, "<< Product Code Already Scanned >>", 3)

    def display_not_isbn_no(self):
        """
        Display message indicating the the product scanned was not a valid ISBN #
        """
        self.sw.clear()
        self.sw.border()
        self.center_label(self.sw, 2, "<< Not an ISBN code >>", 3)

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
                self.book_list.append(book)
            else:
                self.display_not_isbn_no()

        self.redraw_border(self.scr)

    def run(self):
        isbn_text = ""

        self.redraw_border(self.scr)

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

    def init_color_pairs(self):
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
