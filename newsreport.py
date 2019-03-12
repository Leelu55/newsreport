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


def get_top_three_articles():
	db = get_connection()
	c = db.cursor()

	#get slug from path of log table and compare with the articles table slug, then get log counts for titles
	c.execute("create view popular_articles as select count(slug), title from (select split_part(path, '/article/', 2) as log_slug from log) as log_slug_table, articles where log_slug = articles.slug group by title order by count(slug) desc")
	c.execute("select * from popular_articles limit 3")

	rows = c.fetchall()

	for row in rows:
		print(row[0],row[1])

get_top_three_articles()

_connection.close()
