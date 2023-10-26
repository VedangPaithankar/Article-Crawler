import config
import webscraper
import json
from newsapi import NewsApiClient
from pymongo import MongoClient

# Initialize NewsApiClient
api_key = config.api_key
newsapi = NewsApiClient(api_key=api_key)

def analyze(query):
    all_articles = newsapi.get_everything(q=query, language='en', page_size=5)
    extracted_data = []

    for article in all_articles['articles']:
        # Extract article data (similar to your previous code)
        source = article['source']['name']
        url = article['url']
        description = article['description']
        article_text = webscraper.scrape_article_text(url)
        article['text'] = article_text  # Assign article_text to 'text' key in the 'article' dictionary
        published_at = article['publishedAt']
        published_date, published_time = published_at.split('T')
        published_time = published_time[:-1]

        # Create a dictionary for each article
        article_info = {
            'Source': source,
            'Description': description,
            'URL': url,
            'Text': article['text'],  # Access 'text' from the 'article' dictionary
            'Published_Date': published_date,
            'Published_Time': published_time
        }

        # Add the article data to the list
        extracted_data.append(article_info)

    # Don't need to convert to JSON here
    return extracted_data

client = MongoClient(config.mongo)

# Select a database
db = client['Article-Crawler']  # Replace 'Article-Crawler' with the actual name of your database

# Select a collection within the database
collection = db['News']  # Replace 'News' with the actual name of your collection

# Call the submit_query function to retrieve and insert data
extracted_data = analyze('Indian Team')

# Insert the analyzed data into the MongoDB collection
collection.insert_many(extracted_data)

# Close the MongoDB client when you're done
client.close()