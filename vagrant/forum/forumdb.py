#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    #posts.sort(key=lambda row: row['time'], reverse=True)

    posts = []

    # Connect to an existing database
    db = psycopg2.connect("dbname=forum")

    # Open a cursor to perform database operations
    cursor = db.cursor()

    # Query the database and obtain data as Python objects
    query = "SELECT time, content FROM posts ORDER BY time DESC;"
    cursor.execute(query)

    # Method 1: Fetching and iterating over rows separately to populate posts list
    rows = cursor.fetchall()
    for row in rows:
        posts.append({'content': str(bleach.clean(row[1])), 'time': str(row[0])})

    # Method 2: Use inline iterator
    #posts = ({'content': str(bleach.clean(row[1])), 'time': str(row[0])} for row in cursor.fetchall())

    # Shut the connection down
    db.close()

    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    #t = time.strftime('%c', time.localtime())
    #DB.append((t, content))

    # Connect to an existing database
    db = psycopg2.connect("dbname=forum")

    # Open a cursor to perform database operations
    cursor = db.cursor()

    # Set up query to add data to DB
    #
    # Notes:
    #   - Adding comma after the tuple parameter to insert in a safe way to avoid SQL injection bugs.
    #   - Adding bleach.clean() around content variable to prevent things like script injection.
    #
    # Sources:
    #   - http://bobby-tables.com/python.html
    #   - http://initd.org/psycopg/docs/usage.html#the-problem-with-the-query-parameters
    #
    query = "INSERT INTO posts (content) VALUES (%s)"
    cursor.execute(query, (bleach.clean(content),))
    db.commit()
    db.close()
