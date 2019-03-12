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

	#match path to slug by extending slug with "/article/" string, then get log counts for titles, store aggregation and join in a view for reuse
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
	c.execute("""
		select sum(views), authors.name 
			from popular_articles, authors 
		where popular_articles.author = authors.id 
			group by name 
			order by count(views) desc""")

	rows = c.fetchall()
	for row in rows:
		print(row[0], row[1])

def get_high_error_days():
	db = get_connection()
	c = db.cursor()

	c.execute("""
		select count(date(time)), date(time)
			from log 
			where status like '4%'
			group by date(time)
			order by count(date(time))""")

	rows = c.fetchall()
	for row in rows:
		print(row[1], row[0])

get_top_three_articles()
get_top_authors()
get_high_error_days()

_connection.close()
