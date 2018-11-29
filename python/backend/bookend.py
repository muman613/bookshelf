from flask import Flask, render_template
# import bookshelf
from bookshelf import BookShelf, SortBy

app = Flask(__name__)
db = BookShelf()

db.open()

title = "Bookend Book Inventory"

@app.route("/")
@app.route("/index")
def index():
    return "Hello world"

@app.route("/names/<name>")
def hello_name(name):
    return render_template('booklist.html', name=name)

@app.route("/books")
def show_books():
    book_list = []
    db.get_books_to_list(book_list, sortby=SortBy.TITLE)
    return render_template('booklist.html', book_list=book_list, name="Ronald", title=title)


if __name__ == "__main__":
    app.run(debug=True)
