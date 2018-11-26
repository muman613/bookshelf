import psycopg2 as pg

db_name = "bookshelf"
user_name = "bookshelf"
host_name="raspi-mate"
passwd="default"

conn = pg.connect(dbname=db_name, user=user_name, password=passwd, host=host_name)

if conn.status == pg.extensions.STATUS_READY:
    curs = conn.cursor()

    cmd = "SELECT * FROM book_table ORDER BY title;"
    curs.execute(cmd)

    rows = curs.fetchall()


    conn.commit()
    print("OK")

