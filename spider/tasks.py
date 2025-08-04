from bs4 import BeautifulSoup
import re
from celery import Celery
import logging
import urllib.request
import redis
import json
import psycopg2

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
    cursor.execute("CREATE TABLE IF NOT EXISTS pages (url text PRIMARY KEY, links text[], words text[])");
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
             "title": "",
             "words": []}
    for a in soup.find_all('a'):
        link = a.get('href')
        if link:
            link = re.sub("^//", "https://", link)
        parse["links"].append(link)
    for link in parse["links"]:
        if r.get(str(link)) == None:
            parse_page.delay(link)
        
    parse["title"] = soup.title.string
    unfiltered_text = soup.get_text()
    parse["words"] = re.sub("[^\\w]", " ", unfiltered_text).split()
    # Don't drop table students due to unlikely but theoretically possible sql injection
    SQL = "INSERT INTO pages VALUES (%s, %s, %s);"
    data = (url, parse["links"], parse["words"], )
    cursor.execute(SQL, data)
    conn.commit();
    cursor.close();
