from bs4 import BeautifulSoup
import re
from celery import Celery
import logging
import urllib.request
import redis
import json
import psycopg2
import validators

app = Celery('scraper', broker='redis://localhost:6379/0')
r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)



@app.task(rate_limit='60/m')
def parse_page(url):
    conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="development",
                        port="5432")
    cursor = conn.cursor()
    logger = logging.getLogger(__name__)
    logging.info(url)
    html = None
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except:
        logging.error('Failed to parse %s' % url)
        return
    soup = BeautifulSoup(html, 'html.parser')
    parse = {"links": [],
             "content": "",
             "word-tokens": [],
             "title": "",
             "header-tokens": [],}
    for a in soup.find_all('a'):
        link = a.get('href')
        if link:
            # Wikipedia hrefs require wikipedia specific behaviors for reasons
            if "wikipedia" in url:
                link = re.sub("^/wiki", "https://wikipedia.com/wiki", link)
            link = re.sub("^//", "https://", link)
            if validators.url(link):
                parse["links"].append(link)
    for link in parse["links"]:
        if r.get(str(link)) == None:
            parse_page.delay(link)
    parse["title"] = soup.title.string
    parse["title-tokens"] = soup.title.string.split()
    for header in soup.find_all(re.compile("^h[1-6]$")):
        if header.string:
            parse["header-tokens"] += header.string.split()
        
    unfiltered_text = soup.get_text()
    parse["content"] = unfiltered_text
    parse["words"] = re.sub("[^\\w]", " ", unfiltered_text).split()
    # Don't drop table students due to unlikely but theoretically possible sql injection
    SQL = "INSERT INTO pages (url, links, content, word_tokens, title, title_tokens, header_tokens) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO UPDATE SET links = %s, content = %s, word_tokens = %s, title = %s, title_tokens= %s,  header_tokens = %s;"
    data = (url, parse["links"], parse["content"], parse["word-tokens"], parse["title"], parse["title-tokens"], parse["header-tokens"], parse["links"], parse["content"], parse["word-tokens"], parse["title"], parse["title-tokens"], parse["header-tokens"])
    cursor.execute(SQL, data)
    conn.commit();
    cursor.close();

if __name__ == "__main__":
    parse_page("https://en.wikipedia.org/wiki/Black-capped_chickadee")