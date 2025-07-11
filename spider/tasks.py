from bs4 import BeautifulSoup
import re
from celery import Celery
import logging
import urllib.request
import redis
import json

app = Celery('scraper', broker='redis://localhost:6379/0')
r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

@app.task(rate_limit='10/m')
def parse_page(url):
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
    for link in soup.find_all('a'):
        parse["links"].append(link.get('href'))
    for link in parse["links"]:
        if r.get(str(link)) == None:
            parse_page.delay(link)
        
    parse["title"] = soup.title.string
    unfiltered_text = soup.get_text()
    parse["words"] = re.sub("[^\\w]", " ", unfiltered_text).split()
    r.set(str(url), json.dumps(parse))
