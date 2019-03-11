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

	#get slug from path

	c.execute("select title, count(slug) from (select split_part(path, '/article/', 2) as log_slug from log) as log_slug_table, articles where log_slug = articles.slug group by title")
	
	rows = c.fetchall()
	for row in rows:
		print(row[0],row[1])
	# for row in rows:
	# 	if len(row[0]) > 1:
	# 		slugs.append(row[0].partition('/article')[2])

	# for slug in slugs:
	# 	print(slug)


for  row in get_total_200_logs():
	print(row)

strip_path()

_connection.close()


# def add_post(content):
# 	db = psycopg2.connect(database = DBNAME)
# 	c = db.cursor()
# 	content = bleach.clean(content)
# 	c.execute("insert into posts values (%s)", (content,))
# 	db.commit()
# 	db.close()
