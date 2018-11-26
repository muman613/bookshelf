import psycopg2 as pg

db_name = "bookshelf"
user_name = "bookshelf"
host_name="raspi-mate"
passwd="default"

conn = pg.connect(dbname=db_name, user=user_name, password=passwd, host=host_name)

if conn.status == pg.extensions.STATUS_READY:
    # curs = conn.cursor()
    cmd = "INSERT INTO book_table(isbn, title, author) VALUES(%s, %s, %s);"
    # curs.execute(cmd, ('123', '123', '123'))
    # conn.commit()
    with conn as c:
        with c.cursor() as curs:
            curs.execute(cmd, ("123455", "My story", "Michael Uman"))
#    rows = curs.fetchall()

#    conn.commit()
    print("OK")

