# report tool code

import psycopg2
import datetime
import bleach

DBNAME = "news"
_connection = None

def get_connection():
    global _connection
    if not _connection:
        _connection = psycopg2.connect(database = DBNAME)
    return _connection


def get_total_200_logs():
	db = get_connection()
	c = db.cursor()
	c.execute("select path, count(*) as num_200 from log where status = '200 OK' group by path order by num_200 asc")
	rows = c.fetchall()
	return rows

def strip_path():
	db = get_connection()
	c = db.cursor()
	c.execute("select path from log")
	rows = c.fetchall()
	for row in rows:
		print(row)


for  row in get_total_200_logs():
	print(row)

_connection.close()


# def add_post(content):
# 	db = psycopg2.connect(database = DBNAME)
# 	c = db.cursor()
# 	content = bleach.clean(content)
# 	c.execute("insert into posts values (%s)", (content,))
# 	db.commit()
# 	db.close()
