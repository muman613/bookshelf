from flask import Flask, render_template, redirect, send_from_directory, request
from bookshelf.bookshelf import BookShelf, SortBy
import json
import logging

logger = logging.getLogger("bookshelf")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
app.config['SECRET_KEY'] = "mad-money-month"

db = BookShelf()

db.open()

title = "Bookend Book Inventory"

@app.route("/")
@app.route("/index")
def index():
    return redirect("/books")


@app.route("/static/<file>")
def serve_static(file):
    return send_from_directory("static", file)

@app.route("/api/books")
def get_books():
    """
    Return a JSON array of book objects...
    :return:
    """
    sortby_str = request.args.get('sidx', 'title')

    if sortby_str == 'title':
        sort_order = SortBy.TITLE
    elif sortby_str == 'author':
        sort_order = SortBy.AUTHOR
    elif sortby_str == 'isbn':
        sort_order = SortBy.ISBN

    book_list = []
    db.get_books_to_list(book_list, sort_order)

    jsonarray = []
    for book in book_list:
        jsonobj = {
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "pubdate": book.pubdate,
            "pages": book.pages,
            "desc": book.desc,
        }
        jsonarray.append(jsonobj)

    output = json.dumps(jsonarray, indent=4)
    return output

@app.route("/api/book/<isbn>")
def lookup_isbn(isbn):
    # logger.debug("lookup_isbn({})".format(isbn))
    book_list = []
    db.get_books_to_list(book_list)
    jsonobj = {}

    for book in book_list:
        if book.isbn == isbn:
            jsonobj = {
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "pubdate": book.pubdate,
                "pages": book.pages,
                "desc": book.desc,
            }
    output = json.dumps(jsonobj, indent=4)
    return output

@app.route("/books")
def show_books():
    """
    This is the root of the bookshelf system.
    :return:
    """
    logger.debug("show_books()")
    book_list = []
    db.get_books_to_list(book_list, sortby=SortBy.TITLE)
    return render_template('booklist.html', book_list=book_list, title=title)

@app.route("/table")
def show_table():
    """
    This is the root of the bookshelf system.
    :return:
    """
    logger.debug("show_table()")
    return render_template('booktable.html', title=title)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="app.py", description="bookshelf app")
    parser.add_argument("--debug", dest="debug", default=False, action='store_true')
    parser.add_argument("--port", dest="port", default="8000", action='store')
    parser.add_argument("--host", dest="host", default="0.0.0.0", action='store')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    app.run(debug=args.debug, port=args.port, host=args.host)
