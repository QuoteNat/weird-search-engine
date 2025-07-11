from tasks import parse_page, app

if __name__ == "__main__":
    # Seed urls for the scraper to work with
    urls = ["https://wikipedia.com"]
    app.control.rate_limit('myapp.parse_page', '60/m')
    for url in urls:
        parse_page.delay(url)    

