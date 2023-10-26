import requests
from bs4 import BeautifulSoup

def scrape_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Adjust this part based on the specific website's HTML structure
        article_text = ""
        # Extract text content from the HTML (adjust for the specific website)
        for paragraph in soup.find_all('p'):
            article_text += paragraph.text + '\n'
        return article_text
    except Exception as e:
        print(f"Error scraping URL: {url}")
        return ""