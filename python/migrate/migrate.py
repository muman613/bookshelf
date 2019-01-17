import psycopg2 as pg

"""
    This file contains the Python code to migrate from the 1st Schema of the Bookshelf system to the 2nd.
"""

data_servers = {
    "bookshelf": {
        "server": "raspi-mate",
        "user": "bookshelf",
        "db": "bookshelf",
        "pw": "default",
        "conn": None
    },
    "bookshelf2": {
        "server": "localhost",
        "user": "bookshelf",
        "db": "bookshelf2",
        "pw": "default",
        "conn": None
    }
}


def open_connections(server_dict : dict):
    for server_tag in server_dict:
        srvr = server_dict[server_tag]["server"]
        usr = server_dict[server_tag]["user"]
        db = server_dict[server_tag]["db"]
        pw = server_dict[server_tag]["pw"]

        conn = pg.connect(dbname=db, user=usr, password=pw, host=srvr)

        if conn:
            server_dict[server_tag]["conn"] = conn
            print(conn)
        else:
            raise Exception('Bad Server')


def reset_bookshelf2(cur):
    cmd = "DELETE FROM book_table"
    cur.execute(cmd)
    cmd = "DELETE FROM publisher_table"
    cur.execute(cmd)
    cmd = "DELETE FROM author_table"
    cur.execute(cmd)
    cmd = "ALTER SEQUENCE book_table_id_seq RESTART WITH 1"
    cur.execute(cmd)
    cmd = "ALTER SEQUENCE publisher_table_id_seq RESTART WITH 1"
    cur.execute(cmd)
    cmd = "ALTER SEQUENCE author_table_id_seq RESTART WITH 1"
    cur.execute(cmd)

def main():
    try:
        open_connections(data_servers)

        bookshelf_conn = data_servers["bookshelf"]["conn"]
        bookshelf2_conn = data_servers["bookshelf2"]["conn"]

        bookshelf_data = {}

        with bookshelf_conn as connect:
            with connect.cursor() as cur:
                cmd = """
                SELECT * FROM book_table ORDER BY isbn
                """

                cur.execute(cmd)

                bookshelf_data = cur.fetchall()

        with bookshelf2_conn as connect:
            with connect.cursor() as cur:
                reset_bookshelf2(cur)

                for row in bookshelf_data:
                    isbn, title, publisher, author, pubdate, pages, desc, img_link, extra, cat = row
                    print(isbn, " ", title)

                    pub_id = None
                    author_id = None

                    # get publisher if existing in publisher_table

                    cmd = """
                        SELECT id FROM publisher_table WHERE name=%s
                    """

                    cur.execute(cmd, (publisher,))
                    result = cur.fetchone()
                    if result:
                        pub_id = result[0]
                    else:
                        # create publisher
                        cmd = """
                            INSERT INTO publisher_table (name) VALUES (%s) RETURNING id
                        """
                        cur.execute(cmd, (publisher, ))

                        result = cur.fetchall()
                        pub_id = result[0][0]

                    # get author if existing in author_table
                    cmd = """
                        SELECT id from author_table WHERE name=%s
                    """
                    cur.execute(cmd, (author,))
                    result = cur.fetchone()
                    if result:
                        author_id = result[0]
                    else:
                        # create publisher
                        cmd = """
                            INSERT INTO author_table (name) VALUES (%s) RETURNING id
                        """
                        cur.execute(cmd, (author, ))

                        result = cur.fetchall()
                        author_id= result[0][0]


                    cmd = """
                        INSERT INTO book_table (isbn,title,publisher_id,author_id,image_link,description) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """
                    cur.execute(cmd, (isbn, title, pub_id, author_id, img_link, desc[:240]))

                    result = cur.fetchall()

                    print(result)

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
