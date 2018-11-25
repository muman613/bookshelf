# README

This repository contains the Python code to read ISBN # supplied by any barcode scanner capable of scanning ISBN codes. The `scanbook.py` script presents a `curses` based text user interface which waits for ISBN codes to be input via the keyboard (most barcode scanners supply output via a keyboard interface). 

When a code is sent and a carriage return encountered at that point the google book API is queried and if the isbn code is found the information is displayed to the screen.

## TODO

The next steps are:

1) Create a table schema to store the book inventory data.
2) Extract all information from the JSON data and store it in the `PostgreSQL` database.
