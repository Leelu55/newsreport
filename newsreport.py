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
	c.execute("""
		create view popular_articles as 
		select count(log.id) as views, title, author 
			from log, articles 
		where path = concat('/article/',slug) 
			group by title, author 
			order by views desc""")

	c.execute("select * from popular_articles limit 3")

	rows = c.fetchall()
	for row in rows:
		print(row[0],row[1])

def get_top_authors():

	db = get_connection()
	c = db.cursor()

	# use popular_articles view to join with authors table and aggregate the article views for each author
	c.execute("select sum(views), authors.name from popular_articles, authors where popular_articles.author = authors.id group by name order by count(views) desc")

	rows = c.fetchall()
	for row in rows:
		print(row[0], row[1])


get_top_three_articles()
get_top_authors()

_connection.close()
