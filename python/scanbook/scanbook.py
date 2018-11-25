import curses
# from isbntools.app import *
import json
import urllib.request


class BookScanner:
    """
    This class encapsulates the book scanning application. This app has a curses text user interface which
    basically waits for the user to scan in the ISBN barcodes and then looks up the ISBN on the google book API url.
    """

    last_scanned_code = None
    width, height = 0, 0

    def __init__(self, scr):
        self.scr = scr
        self.height, self.width = scr.getmaxyx()

        sw = scr.subwin(self.height - 20, self.width - 20, 10, 10)
        sw.bkgd(" ", curses.color_pair(2))
        sw.border()
        self.sw = sw

    @staticmethod
    def get_isbn_google_api(isbn: str):
        """
        Look up the ISBN # on the google book API. The server returns to us a JSON formatted file which we use
        to extract the relevant information.
        :param isbn: ISBN # to look-up
        :return: Dictionary containing the parsed Json.
        """
        urlbase = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

        fullurl = urlbase + isbn

        with urllib.request.urlopen(fullurl) as url:
            data = json.loads(url.read().decode())

        if "items" in data:
            return data["items"][0]["volumeInfo"]
        else:
            return None

    def draw_isbn(self, isbn: str, metadata=None):
        label = "Last ISBN # Scanned : {:14}".format(isbn)
        self.center_label(self.scr, 6, label)
        if metadata:
            self.sw.clear()
            self.sw.border()

            title = metadata["title"]
            publisher = metadata["publisher"]
            authors = ",".join(metadata["authors"])
            pub_date = metadata["publishedDate"]

            label = "Title     : {:60}".format(title)
            self.sw.addstr(2, 10, label)
            label = "Publisher : {:60}".format(publisher)
            self.sw.addstr(3, 10, label)
            label = "Author(s) : {:60}".format(authors)
            self.sw.addstr(4, 10, label)
            label = "Published : {:60}".format(pub_date)
            self.sw.addstr(5, 10, label)

    def center_label(self, scr, y: int, label: str, pair: int= 0):
        h, w = scr.getmaxyx()

        scr.addstr(y, int((w - len(label)) / 2), label, curses.color_pair(pair))

    def redraw_border(self, scr):
        self.scr.border()
        self.center_label(self.scr, 0, "Book Scanning Application", 1)
        self.center_label(self.scr, 1, "By Michael Uman", 1)
        self.center_label(self.scr, self.height - 2, "Hit 'q' to exit")

    @staticmethod
    def dump_isbn(metadata):
        """
        Dump the JSON data to the file /tmp/isbn.data.
        :param metadata: json data to dump
        """
        with open("/tmp/isbn.data", "a+") as fp:
            json.dump(metadata, fp, indent=4)
            fp.write("\n")

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

    def handle_scanned_code(self, isbn: str):
        if self.last_scanned_code == isbn:
            self.display_product_rescan()
        else:
            data = BookScanner.get_isbn_google_api(isbn)
            if data:
                BookScanner.dump_isbn(data)
                self.draw_isbn(isbn, data)
                self.last_scanned_code = isbn
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
                    # draw_isbn(stdscr, isbn_text)
                    self.handle_scanned_code(isbn_text)
                    isbn_text = ""

def init_color_pairs():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_RED)


def bookshelf_main(stdscr):
    global width, height

    init_color_pairs()
    curses.curs_set(0)

    # curses.cbreak()

    stdscr.nodelay(True)
    stdscr.border()

    scanner = BookScanner(stdscr)

    scanner.run()

    # height, width = stdscr.getmaxyx()
    #
    # redraw_border(stdscr)

    isbn_text = ""


    # while True:
    #     stdscr.refresh()
    #
    #     s = stdscr.getch()
    #     if s != -1:
    #         if s == ord("q"):
    #             break
    #         elif ord("0") <= s <= ord("9"):
    #             isbn_text += chr(s)
    #         elif s == ord("\n"):
    #             #draw_isbn(stdscr, isbn_text)
    #             handle_scanned_code(stdscr, isbn_text)
    #             isbn_text = ""


def main():
    curses.wrapper(bookshelf_main)


if __name__ == "__main__":
    main()
