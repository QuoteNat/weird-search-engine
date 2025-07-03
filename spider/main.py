from bs4 import BeautifulSoup

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    parse = {"links": [],
             "title": "",
             "words": []}
    for link in soup.find_all('a'):
        parse["links"].append(link.get('href'))
        
    return parse

def main():
    print("Hello from spider!")


if __name__ == "__main__":
    main()