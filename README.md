# SearchFind

A small search engine built from scratch, no Elasticsearch, no search libraries, no JavaScript frameworks. Just Python, PostgreSQL, and a lot of debugging.

It crawls a set of real web pages, indexes them into a database, and ranks search results using TF-IDF (the same basic math early search engines used before things like PageRank existed).

## What it does

- Type a word or phrase into the search box, get back real ranked results
- "I'm Feeling Lucky" jumps straight to the top result instead of showing the list
- Results are ranked by relevance, not just by whether the word appears
- Styled like an old-school 1990s search engine, on purpose

## How it works

```
Web pages --> crawler --> dataCrawler.json --> PostgreSQL --> TF-IDF ranking --> Flask --> results page
```

1. `processPages.py` / `runCrawler.py` fetch pages with `requests`, strip the HTML down to plain text with BeautifulSoup, and count word frequency per page.
2. `importData.py` loads that data into a PostgreSQL database with three tables: `documents`, `terms`, and `docTermFrequency`.
3. `app.py` runs a Flask server. When you search, it runs a SQL query that scores every matching page using TF-IDF and returns them ranked highest first.
4. Jinja2 templates render the results into the retro-styled HTML pages.

## Tech used

- Python, Flask, Jinja2
- PostgreSQL, psycopg2
- requests, BeautifulSoup
- Plain HTML/CSS (no JS frameworks, on purpose)

## Running it locally

1. Install PostgreSQL and create a database.
2. Create the three tables (`documents`, `terms`, `docTermFrequency`) — see the SQL in `schema.sql` if included, or the project docs.
3. Add a `.env` file with your database password:
   ```
   POSTGRES_PASSWORD=yourpassword
   ```
4. Install the Python dependencies:
   ```
   pip install flask psycopg2-binary python-dotenv requests beautifulsoup4
   ```
5. Run the crawler to generate `dataCrawler.json`:
   ```
   python runCrawler.py
   ```
6. Import the crawled data into the database:
   ```
   python importData.py
   ```
7. Start the app:
   ```
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.

## What it's missing (on purpose, for now)

- No description/snippet text under results — the crawler only saves URL, title, and word counts right now
- Crawls a fixed list of URLs, doesn't follow links automatically
- No phrase search or excluding words yet
- Runs on Flask's dev server, not meant for production

## Why I built it this way

This was a learning project, the point was to actually understand how a search engine works instead of plugging one together. Every part — the crawler, the database schema, the ranking formula, the Flask routes — was built and debugged by hand.
