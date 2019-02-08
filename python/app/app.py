"""
    BookShelf App Version 1.0
    By Michael A. Uman (C) 2019 HUman DevTools
"""

from flask import Flask, render_template, redirect, send_from_directory, request, session, flash, url_for
from flask_cors import CORS, cross_origin
from bookshelf.bookshelf import BookShelf, SortBy
import json
import logging
from functools import wraps
import os
import argparse

options = argparse.Namespace()

logger = logging.getLogger("bookshelf")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
app.config['SECRET_KEY'] = "mad-money-month"

title = "Bookend Book Inventory"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('show_books'))
    return render_template('login.html', error=error, title='Login Page')


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


@app.route("/static/<file>")
def serve_static(file):
    return send_from_directory("static", file)


@app.route("/api/books", methods=[ 'GET', 'POST'])
@login_required
@cross_origin()
def get_books():
    """
    Return a JSON array of book objects...
    :return:
    """

    output = ''

    if request.method == 'GET':
        sortby_str = request.args.get('sidx', 'title')

        if sortby_str == 'title':
            sort_order = SortBy.TITLE
        elif sortby_str == 'author':
            sort_order = SortBy.AUTHOR
        elif sortby_str == 'isbn':
            sort_order = SortBy.ISBN

        book_list = []
        app.db.get_books_to_list(book_list, sort_order)

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
    elif request.method == 'POST':
        if 'oper' in request.values and request.values['oper'] == 'edit':
            isbn = request.values['isbn']
            title = request.values['title']
            author = request.values['author']
            publisher = request.values['publisher']

            edit_book = app.db.get_book(isbn)
            print(edit_book)
            edit_book.title = title
            edit_book.author = author
            edit_book.publisher = publisher

            app.db.update_book(edit_book)

            output = json.dumps("{ status: 'Success' }")
        else:
            pass

    return output

@app.route("/api/book/<isbn>")
@login_required
@cross_origin()
def lookup_isbn(isbn):
    # logger.debug("lookup_isbn({})".format(isbn))
    book_list = []
    app.db.get_books_to_list(book_list)
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

@app.route("/")
@login_required
def show_books():
    """
    This is the root of the bookshelf system.
    :return:
    """
    logger.debug("show_books()")
    book_list = []
    app.db.get_books_to_list(book_list, sortby=SortBy.TITLE)
    return render_template('booklist.html', book_list=book_list, title=title)

@app.route("/table")
@login_required
def show_table():
    """
    This is the root of the bookshelf system.
    :return:
    """
    logger.debug("show_table()")
    return render_template('booktable.html', title='jqQuery Table')


def initdb():
    logger.debug('initdb() -- initializing database')

    DB_NAME = "bookshelf"
    app.db = BookShelf(dbase=DB_NAME, host=options.db_host, user=options.db_user,  pwd=options.db_pass)
    app.db.open()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="app.py", description="bookshelf app")

    parser.add_argument("--debug",
                        dest="debug",
                        default=False,
                        action='store_true')
    parser.add_argument("--web-port",
                        dest="app_port",
                        default=os.getenv('BOOKSHELF_WEB_PORT', '8000'),
                        action='store')
    parser.add_argument("--web-host",
                        dest="app_host",
                        default=os.getenv('BOOKSHELF_WEB_HOST', '0.0.0.0'),
                        action='store')
    parser.add_argument("--db-host",
                        dest='db_host',
                        default=os.getenv('BOOKSHELF_DB_HOST', 'laserquad.ddns.net'),
                        action='store')
    parser.add_argument("--db-user",
                        dest='db_user',
                        default=os.getenv('BOOKSHELF_DB_USER', 'bookshelf_user'),
                        action='store')
    parser.add_argument("--db-password",
                        dest='db_pass',
                        default=os.getenv('BOOKSHELF_DB_PASS', 'default'),
                        action='store')
    
    args = parser.parse_args(namespace=options)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Initialize the apps database object
    initdb()

    app.run(debug=args.debug, port=args.app_port, host=args.app_host)
