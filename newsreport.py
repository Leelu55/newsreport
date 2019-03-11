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


def strip_path():
	db = get_connection()
	c = db.cursor()

	#get slug from path of log table and compare with the articles table slug, then get log counts for titles
	c.execute("select title, count(slug) from (select split_part(path, '/article/', 2) as log_slug from log) as log_slug_table, articles where log_slug = articles.slug group by title order by count(slug) desc limit 3")
	
	rows = c.fetchall()
	for row in rows:
		print(row[0],row[1])


strip_path()

_connection.close()


# def add_post(content):
# 	db = psycopg2.connect(database = DBNAME)
# 	c = db.cursor()
# 	content = bleach.clean(content)
# 	c.execute("insert into posts values (%s)", (content,))
# 	db.commit()
# 	db.close()
