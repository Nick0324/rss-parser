import feedparser
import time


def get_articles(url):
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'description': entry.summary,
            'time': entry.published_parsed
        }
        article['time'] = time.strftime('%Y-%m-%d %H:%M:%S', article['time'])
        articles.append(article)

    return articles
