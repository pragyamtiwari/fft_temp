# https://docs.python.org/3/library/json.html
# This library will be used to parse the JSON data returned by the API.
import json
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request

apikey = "3a17e828f28b1276d0a1241a08ff84aa"
url = f"https://gnews.io/api/v4/search?q=indian+politics&lang=en&country=us&max=10&apikey={apikey}"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))
    articles = data["articles"]

    for i in range(len(articles)):
        print(f"Title: {articles[i]['title']}")
        print(f"Description: {articles[i]['description']}")
        print(f"URL: {articles[i]['url']}")
        print("-" * 50)