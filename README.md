# README

This repository contains the Python code to read ISBN # supplied by any barcode scanner capable of scanning ISBN codes. The `scanbook.py` script presents a `curses` based text user interface which waits for ISBN codes to be input via the keyboard (most barcode scanners supply output via a keyboard interface). 

When a code is sent and a carriage return encountered at that point the google book API is queried and if the isbn code is found the information is displayed to the screen. The book information is then written to the database back-end.

# Demo

If my Amazon EC2 Instance is up and running you should be able to view the flask application running @

http://ec2-13-58-147-207.us-east-2.compute.amazonaws.com/bookshelf/books

## Database back-end

The `bookshelf` application uses a `PostgreSQL` database back-end to store all the books in the bookshelf. In my set-up I am running a PostgreSQL server on a Raspberry Pi 3 host which is accessible within my local network.

To customize this application to run in another environment you can change the database host, user, database name, and password in the  `BookScanner` class.

The application works with the user `bookshelf` and the database `bookshelf` which has the default password.

## TODO

* Create the database if it doesn't exist.
* Provide RESTful API for web interface.
* Handle screen resize gracefully ( https://docs.python.org/3/library/curses.html#constants )
