import requests

url = "https://en.wikipedia.org/wiki/Timeline_of_web_search_engines"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(f"Success!\nStatus code: {response.status_code}")

    with open("searchEngineWiki.html", "w", encoding="utf-8") as file:
        file.write(response.text)

else:
    print(f"Failed!\nStatus code: {response.status_code}")
