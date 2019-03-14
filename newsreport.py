#!/usr/bin/env python3

import psycopg2

DBNAME = "news"
_connection = None


# establish new db connection if it doesn't exist yet, otherwise return it
def get_connection():
    global _connection
    if not _connection:
        _connection = psycopg2.connect(database=DBNAME)
    return _connection


def get_top_three_articles():
    db = get_connection()
    c = db.cursor()

# match path to slug by extending slug with "/article/" string,
# get log counts for titles, store aggregation and join in a view for reuse
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
        print("\"{0:s}\" —  {1:d} views".format(row[1], row[0]))

    print("\n")


def get_top_authors():

    db = get_connection()
    c = db.cursor()

    # use popular_articles view to join with authors table and
    # aggregate the article views for each author with sum
    c.execute("""
        select sum(views), authors.name
            from popular_articles, authors
        where popular_articles.author = authors.id
            group by name
            order by count(views) desc""")

    rows = c.fetchall()
    for row in rows:
        print("{0:s} — {1:f} views".format(row[1], row[0]))

    print("\n")


def get_high_error_days():
    db = get_connection()
    c = db.cursor()

    # agrregate total logs per day and error logs per day with two subselects,
    # from joining total_log_view and error_per_date_view select days
    # where ratio of error logs > 1%
    c.execute("""
        select ((num_error_logs * 100)::numeric/num_total_logs) as error_ratio,
                total_date
            from
        (
            select count(date(time)) as num_total_logs, date(time) as total_date
                from log
            group by date(time)
            order by date(time)
        ) as total_log_view,
        (
            select count(date(time)) as num_error_logs, date(time) as error_date
                from log
            where status like '4%'
                group by date(time)
                order by count(date(time))
        ) as error_per_date_view
        where  total_date = error_date and
                ((num_error_logs * 100)::numeric/num_total_logs) > 1
            group by error_ratio, total_date
        """)

    rows = c.fetchall()
    for row in rows:
        print("{0:s} — {1:f}% errors".format(
            row[1].strftime('%B %d, %Y'), round(row[0], 2)))


get_top_three_articles()
get_top_authors()
get_high_error_days()

_connection.close()
