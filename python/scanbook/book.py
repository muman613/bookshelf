import json
import urllib.request


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

    if ("items" in data) and ("volumeInfo" in data["items"][0]):
        return data["items"][0]["volumeInfo"]
    else:
        return None


class Book:
    """
    The book class is used to encapsulate the properties of a book.
    """

    def __init__(self, isbn = None):
        """
        If an isbn # is passed to the constructor it will look up the ISBN # using the google book API.
        :param isbn: string representing the ISBN, will be None if no parameter is passed.
        """
        self.data = {
            "isbn": None,
            "title": None,
            "author": None,
            "publisher": None,
            "pubdate": None,
            "pages": 0,
            "desc": "",
            "image": None
        }

        if isbn:
            self.load_from_google(isbn)

    def load_from_google(self, isbn: str):
        """
        Get the data in JSON format from the google API and fill in the classes data dictionary.
        :param isbn:
        :return:
        """
        google_data = get_isbn_google_api(isbn)
        if google_data:
            Book.dump_isbn(google_data)

            self.data["isbn"] = isbn
            self.data["title"] = google_data["title"] if "title" in google_data else "N/A"
            authors = ", ".join(google_data["authors"]) if "authors" in google_data else "N/A"
            self.data["author"] = authors
            self.data["publisher"] = google_data["publisher"] if "publisher" in google_data else "N/A"
            self.data["pubdate"] = google_data["publishedDate"] if "publishedDate" in google_data else "N/A"
            self.data["pages"] = google_data["pageCount"] if "pageCount" in google_data else "N/A"
            self.data["desc"] = google_data["description"] if "description" in google_data else "N/A"
            self.data["image"] = google_data["imageLinks"]["thumbnail"] if "imageLinks" in google_data else "N/A"

    def __getitem__(self, item):
        # print("getitem({})".format(item))
        if item in self.data.keys():
            return self.data[item]
        else:
            return None

    def __getattr__(self, item):
        # print("getattr({})".format(item))
        if item in self.data.keys():
            return self.data[item]
        else:
            raise IndexError

    def __setitem__(self, key, value):
        # print("setitem({}, {})".format(key, value))
        if key in self.data.keys():
            self.data[key] = value
        else:
            raise IndexError

    def __setattr__(self, key, value):
        if key == "data":
            self.__dict__["data"] = value
        elif key in self.data.keys():
            self.__dict__["data"][key] = value
        else:
            raise IndexError

    def __repr__(self):
        return "{{ {}, \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\" }}".format(self.data["isbn"], self.data["title"],
                                                                 self.data["author"], self.data["publisher"],
                                                                 self.data["pubdate"], self.data["pages"],
                                                                 self.data["desc"][:60])

    def __bool__(self):
        return self.data["isbn"] is not None and self.data["title"] is not None

    def __eq__(self, other):
        return self.data["isbn"] == other["isbn"]

    @staticmethod
    def dump_isbn(metadata):
        """
        Dump the JSON data to the file /tmp/isbn.data.
        :param metadata: json data to dump
        """
        with open("/tmp/isbn.data", "a+") as fp:
            json.dump(metadata, fp, indent=4)
            fp.write("\n")


def main():
    book = Book("9781491933176")

    print("Title : {}".format(book.title))

    print(book)

    print("-" * 80)

    books = [
        Book("9781491933176"),
        Book("9781849691505")
    ]

    for mybook in books:
        print(mybook)

    print("-" * 80)

#   Here we will set the values of the title & author of the books stored in the list...
    books[0].title = "Superman VS Batman"
    books[1].author = "Godzilla & King Kong"

    for mybook in books:
        print(mybook)

    print("-" * 80)

#   Here we will manually craft a book object and fill in the information

    newbook = Book()
    newbook.isbn = "9123123123121"
    newbook.title = "Advanced C/C++ Programming for Embedded Systems"
    newbook.author = "James Pollack"
    newbook.publisher = "O'Reilly & Son"
    newbook.pubdate = "2016"

    if newbook:
        print(newbook)
        print("-" * 80)

    books.append(newbook)

    for mybook in books:
        print(mybook)

    print("-" * 80)


if __name__ == "__main__":
    main()
