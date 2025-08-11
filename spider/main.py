from tasks import parse_page, app
import psycopg2

if __name__ == "__main__":
    conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="development",
                        port="5432")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pages (url text PRIMARY KEY, links text[], words text[], title text[], headers text[])");
    conn.commit();
    cursor.close();
    # Ensure that pages table exists
    # Seed urls for the scraper to work with
    urls = ["https://wikipedia.com", "https://npr.org", "https://en.wikipedia.org/wiki/Black-capped_chickadee"]
    app.control.rate_limit('tasks.parse_page', '60/m')
    for url in urls:
        parse_page.delay(url)    

