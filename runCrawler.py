import json

from processPages import process_url

urls = [
    "https://en.wikipedia.org/wiki/Web_search_engine",
    "https://en.wikipedia.org/wiki/Information_retrieval",
    "https://en.wikipedia.org/wiki/Web_crawler",
    "https://en.wikipedia.org/wiki/Tf-idf",
    "https://en.wikipedia.org/wiki/Okapi_BM25",
    "https://en.wikipedia.org/wiki/Search_engine_indexing",
    "https://en.wikipedia.org/wiki/PageRank",
    "https://en.wikipedia.org/wiki/Google_Search",
    "https://en.wikipedia.org/wiki/WebCrawler",
    "https://en.wikipedia.org/wiki/Internet",
    "https://en.wikipedia.org/wiki/World_Wide_Web",
    "https://en.wikipedia.org/wiki/Search_engine_optimization",
    "https://en.wikipedia.org/wiki/Computer_science",
    "https://en.wikipedia.org/wiki/Web_scraping",
    "https://www.w3.org/TR/REC-html32",
    "https://www.robotstxt.org/robotstxt.html",
    "https://requests.readthedocs.io/en/latest/",
    "http://infolab.stanford.edu/pub/papers/google.pdf",
    "https://en.wikipedia.org/wiki/Inverted_index",
    "https://www.retro-engine-fake-domain-test.local"
]

results = []

for url in urls:
    try:
        result = process_url(url)
        if result is not None:
            results.append(result)
    except Exception as e:
        print(f"Failed to Retrieve: {url}")
        print(f"Error: {e}")
print(f"Successful pages: {len(results)}")

with open("dataCrawler.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)
