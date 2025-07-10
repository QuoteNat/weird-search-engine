from bs4 import BeautifulSoup
import re
from celery import Celery
import logging
import urllib.request

app = Celery('scraper', broker='redis://localhost:6379/0')
logger = logging.getLogger(__name__)

@app.task
def parse_page(url):
    html = None
    with urllib.request.urlopen(url) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    parse = {"links": [],
             "title": "",
             "words": []}
    for link in soup.find_all('a'):
        parse["links"].append(link.get('href'))
    parse["title"] = soup.title.string
    unfiltered_text = soup.get_text()
    parse["words"] = re.sub("[^\\w]", " ", unfiltered_text).split()
    logging.info(parse)
    return parse

if __name__ == "__main__":
    app.start()
    urls = ["https://wikipedia.com"]
    for url in urls:
        parse_page.delay(url)    

