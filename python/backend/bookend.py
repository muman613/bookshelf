from flask import Flask, render_template, redirect, send_from_directory
# import bookshelf
from bookshelf import BookShelf, SortBy
import json

app = Flask(__name__)
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


@app.route("/book/<isbn>")
def lookup_isbn(isbn):
    book_list = []
    db.get_books_to_list(book_list)
    jsonobj = {}

    for book in book_list:
        if book.isbn == isbn:
            jsonobj = {
                "isbn": book.isbn,
                "title": book.title,
                "publisher": book.publisher,
                "pubdate": book.pubdate,
                "pages": book.pages,
                "desc": book.desc,
            }
    output = json.dumps(jsonobj, indent=4)
    return output

@app.route("/books")
def show_books():
    book_list = []
    db.get_books_to_list(book_list, sortby=SortBy.TITLE)
    return render_template('booklist.html', book_list=book_list, title=title)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
