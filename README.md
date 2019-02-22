# README

This repository contains the Python code to read ISBN # supplied by any barcode scanner capable of scanning ISBN codes. The `scanbook.py` script presents a `curses` based text user interface which waits for ISBN codes to be input via the keyboard (most barcode scanners supply output via a keyboard interface). 

When a code is sent and a carriage return encountered at that point the google book API is queried and if the isbn code is found the information is displayed to the screen. The book information is then written to the database back-end.

## Database back-end

The `bookshelf` application uses a `PostgreSQL` database back-end to store all the books in the bookshelf. In my set-up I am running a PostgreSQL server on a Raspberry Pi 3 host which is accessible within my local network.

To customize this application to run in another environment you can change the database host, user, database name, and password in the  `BookScanner` class.

The application works with the user `bookshelf` and the database `bookshelf` which has the default password.

# Docker Container

A `DockerFile` has been provided which sets up a container image running the Flask application. This container exposes the TCP port 8000 on the local machine. This container has been built for Raspberry Pi 3.

    # Use an official Python runtime as a parent image
    FROM python:3
    
    # Set the working directory to /app
    WORKDIR /app
    
    # Copy the current directory contents into the container at /app
    COPY app/app.py ./
    COPY app/static ./static/
    COPY app/templates ./templates/
    COPY bookshelf ./bookshelf/
    COPY requirements.txt ./
    
    # Install any needed packages specified in requirements.txt
    RUN pip install --trusted-host pypi.python.org -r requirements.txt
    
    # Make port 80 available to the world outside this container
    EXPOSE 8000
    
    # Run app.py when the container launches
    CMD ["python", "app.py"]

# RESTful API

The `bookshelf` application now provides a special end-point containing the API. This API provides JSON data for all the books in the database or just the data for one particular book. Currently the API is not documented.

## TODO

* Create the database if it doesn't exist.
* Document the RESTful API
* Handle screen resize gracefully ( https://docs.python.org/3/library/curses.html#constants )
* Support passing password in via environment variable.
* Use sqlalchemy ORM database module for DB access.
* New schema in Bookshelf 2.0 coming soon.
