import feedparser
import time
import sqlite3


def get_articles(url):
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'description': entry.summary,
            'time': time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed),
            'author': entry.get("author", ""),
            'categories': [tag.term for tag in entry.get("tags", [])]
        }
        articles.append(article)

    return articles


def add_articles_to_database(articles):
    conn = sqlite3.connect('articles.db')

    # Define a table schema
    conn.execute("CREATE TABLE IF NOT EXISTS articles(title, author, link, description, categories)")

    # Insert data from each article into the database
    for article in articles:
        categories_str = '|'.join(article['categories'])
        conn.execute('''
            INSERT INTO articles (title, author, link, description, categories)
            VALUES (?, ?, ?, ?, ?)
        ''', (article['title'], article['author'], article['link'], article['description'], categories_str))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
