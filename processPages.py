import requests
from bs4 import BeautifulSoup
from cleanText import clean_html

def process_url(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    for tag in soup(["script", "style"]):
        tag.decompose()

    title = soup.title.get_text(strip=True)
    
    text = soup.get_text(" ", strip=True)
    
    snippet = text[:300]   

    wordCount = clean_html(response.text)

    result = {
        "url": url,
        "title": title,
        "snippet": snippet,
        "word_counts": wordCount
    }

    return result


result = process_url(
    "https://en.wikipedia.org/wiki/Timeline_of_web_search_engines"
)

print(result["title"])
print(result["snippet"])
print(len(result["word_counts"]))
