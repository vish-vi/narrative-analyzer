import sqlite3
import requests 
import os
from dotenv import load_dotenv
import database


# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')

def get_articles(topic, count=10):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "pageSize": count,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    article_ids = []
    conn = sqlite3.connect('news_analysis.db')
    for article in data.get("articles", []):
        # Capture the newly inserted primary key ID
        article_id = database.insert_article(conn, topic, article['title'], article['description'], article['content'], article['source']['name'], article['url'], article['publishedAt'])
        article_ids.append(article_id)
    conn.close()
    return article_ids  # Return IDs so main.py knows what to analyze

