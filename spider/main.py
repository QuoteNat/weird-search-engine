from bs4 import BeautifulSoup
import re

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    parse = {"links": [],
             "title": "",
             "words": []}
    for link in soup.find_all('a'):
        parse["links"].append(link.get('href'))
    parse["title"] = soup.title.string
    unfiltered_text = soup.get_text()
    parse["words"] = re.sub("[^\\w]", " ", unfiltered_text).split()
    return parse

def main():
    print("Hello from spider!")


if __name__ == "__main__":
    main()