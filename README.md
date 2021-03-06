# News Report Log Analysis Project 

This Python program analyses the PostgreSQL database **news** provided in context with the [Full Stack Web Developer Nanodegree Program](https://eu.udacity.com/course/full-stack-web-developer-nanodegree--nd004) for answering the following questions:

- What are the most popular three articles of all time?
- Who are the most popular article authors of all time? 
- On which days did more than 1% of requests lead to errors?

## Dependencies

The Program uses the Python3 Python release and Psycopg2 PostgreSQL adapter for Python 

#### 1. Install [Python3](https://www.python.org/downloads/release/python-372/) in the latest version if you don't have it yet. 
You can check for your Python version with ```python -V```

**Installation on Ubuntu:**

``` sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
```

#### 2. Install [Psycopg2](http://initd.org/psycopg/)

**Installation on Ubuntu with Python3**

```sudo apt install libpq-dev python3-dev```

## Getting Started

1. Download the [news.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) file, uzip it and run `psql -d news -f newsdata.sql` to import the data.
2. Copy the Python Script **newsreport.py** into the directory of the **news** database. 
4. Run `python3 newsreport.py` to get the analysis of the database for the given questions.

## Documentation

The program runs three functions, each of them answering one of the questions by opening or reusing a connection to the news database and executing an SQL query.

### get_top_three_articles() 

#### 1. Create a popular articles view:

```
CREATE VIEW popular_articles AS
SELECT count(log.id) AS views,
       title,
       author
FROM log,
     articles
WHERE PATH = concat('/article/', slug)
GROUP BY title,
         author
ORDER BY views DESC
```

- joins the log and the articles database matching the log path (f.ex. _/article/media-obsessed-with-bears_) to the article slug (_media-obsessed-with-bears_) by concatenating the slug with _/article/_
- agrregates the logs by counting all views for an article (f.ex. _/article/candidate-is-jerk'_ has 338647 views)
- creates the view  **popular_articles** with the columns **views** (the aggregated log entries per article), **title** (of the article) and **author** (id of the article author)

#### 2. Use the popular_articles view for displaying the most popular 3 articles
```
SELECT *
FROM popular_articles
LIMIT 3
```

### get_top_authors()

Display the most popular authors:

```
SELECT sum(views),
       authors.name
FROM popular_articles,
     authors
WHERE popular_articles.author = authors.id
GROUP BY name
ORDER BY count(views) DESC
```
Uses the **popular_articles** view, joins it with the authors table and aggregates views per author.

### get_high_error_days()

Find days with more than 1% error requests:

```
SELECT ((num_error_logs * 100)::numeric/num_total_logs) AS error_ratio, 
	total_date
FROM
  (SELECT count(date(TIME)) AS num_total_logs,
          date(TIME) AS total_date
   FROM log
   GROUP BY date(TIME)
   ORDER BY date(TIME)) AS total_log_view,

  (SELECT count(date(TIME)) AS num_error_logs,
          date(TIME) AS error_date
   FROM log
   WHERE status LIKE '4%'
   GROUP BY date(TIME)
   ORDER BY count(date(TIME))) AS error_per_date_view
WHERE total_date = error_date
  AND ((num_error_logs * 100)::numeric/num_total_logs) > 1
GROUP BY error_ratio,
         total_date
```
Calculates the error ratio from 2 subselects, one finding the total requests per day and the other the error requests per day (by querying the status column, filtering for 4xx HTTP status codes). The results of these to subselects are used to calculate the ratio of errors to requests. All days with an error ratio > 1 are displayed. 

## Common Usage

```
newsreport$ python3 newsreport.py
"Candidate is jerk, alleges rival" —  338647 views
"Bears love berries, alleges bear" —  253801 views
"Bad things gone, say good people" —  170098 views


Ursula La Multa — 507594 views
Rudolf von Treppenwitz — 423457 views
Anonymous Contributor — 170098 views
Markoff Chaney — 84557 views


July 17, 2016 — 2.26% errors
```



