from flask import Flask, render_template, request
from scraper import get_articles, add_articles_to_database
import json

app = Flask(__name__)

# Load articles from the scraper
articles = get_articles('https://rss.nytimes.com/services/xml/rss/nyt/World.xml')

add_articles_to_database(articles)

# Write articles to JSON file
with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False)


@app.route('/articles')
def get_articles_route():
    # Get search query from request parameters
    search_query = request.args.get('q')

    # Filter articles by search query
    if search_query:
        filtered_articles = [a for a in articles if search_query.lower() in a['title'].lower()]
    else:
        filtered_articles = articles

    # Get sort type from request parameters
    sort_type = request.args.get('sort')

    # Get sort order from request parameters
    sort_order = request.args.get('order')

    # Sort articles by date or alphabetically
    if sort_type == 'title' and sort_order == 'asc':
        sorted_articles = sorted(filtered_articles, key=lambda a: a['title'].lower())
    elif sort_type == 'title' and sort_order == 'desc':
        sorted_articles = sorted(filtered_articles, key=lambda a: a['title'].lower(), reverse=True)
    elif sort_type == 'time' and sort_order == 'asc':
        sorted_articles = sorted(filtered_articles, key=lambda a: a['time'])
    else:
        sorted_articles = sorted(filtered_articles, key=lambda a: a['time'], reverse=True)

    return render_template('articles.html', articles=sorted_articles)


if __name__ == '__main__':
    app.run()
