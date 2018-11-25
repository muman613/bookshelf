import curses
from isbntools.app import *
import json
import urllib.request


# stdscr = None
last_scanned_code = None
width, height = 0, 0


def get_isbn_google_api(isbn: str):
    urlbase = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    fullurl = urlbase + isbn

    with urllib.request.urlopen(fullurl) as url:
        data = json.loads(url.read().decode())

    return data["items"][0]["volumeInfo"]


def draw_isbn(scr, isbn, metadata=None):
    label = "Last ISBN # Scanned : {:14}".format(isbn)
    center_label(scr, 2, label)
    if metadata:
        title = metadata["title"]
        publisher = metadata["publisher"]

        label = "Title     : {:60}".format(title)
        scr.addstr(11, 20, label)
        label = "Publisher : {:60}".format(publisher)
        scr.addstr(12, 20, label)

def center_label(scr, y: int, label: str, pair: int= 0):
    global height, width
    scr.addstr(y, int((width - len(label)) / 2), label, curses.color_pair(pair))


def redraw_border(scr):
    scr.border()
    center_label(scr, 0, "Book Scanning Application", 1)


def dump_isbn(metadata):
    with open("/tmp/isbn.data", "a+") as fp:
        json.dump(metadata, fp, indent=4)
        fp.write("\n")


def handle_scanned_code(scr, isbn: str):
    global last_scanned_code

    if last_scanned_code == isbn:
        scr.move(2, 1)
        scr.clrtoeol();
        center_label(scr, 2, "<< Product Code Already Scannned >>", 2)
    else:
        # data = meta(isbn)
        data = get_isbn_google_api(isbn)

        dump_isbn(data)
        draw_isbn(scr, isbn, data)

    redraw_border(scr)
    last_scanned_code = isbn


def init_color_pairs():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)


def bookshelf_main(stdscr):
    global width, height

    init_color_pairs()
    curses.curs_set(0)

    # curses.cbreak()

    stdscr.nodelay(True)
    stdscr.border()

    height, width = stdscr.getmaxyx()

    redraw_border(stdscr)

    isbn_text = ""

    sw = stdscr.subwin(height - 20, width - 20, 10, 10)
    sw.bkgd(" ", curses.color_pair(2))
    sw.addstr(2, 2, "Shit")
    sw.border()

    while True:
        stdscr.refresh()

        s = stdscr.getch()
        if s != -1:
            if s == ord("q"):
                break
            elif ord("0") <= s <= ord("9"):
                isbn_text += chr(s)
            elif s == ord("\n"):
                #draw_isbn(stdscr, isbn_text)
                handle_scanned_code(stdscr, isbn_text)
                isbn_text = ""


def main():
    curses.wrapper(bookshelf_main)


if __name__ == "__main__":
    main()
