import os
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

import requests

from workflow.models import Headline
from workflow.config import NUM_SERP_RESULTS, SERP_FRESHNESS


def get_interest_headlines(interest):
    interest_name_parsed = interest.name.replace(" ", "+")
    num_results = NUM_SERP_RESULTS

    url = f"https://google.serper.dev/news?q={interest_name_parsed}&num={num_results}&tbs=qdr%3A{SERP_FRESHNESS}&apiKey={SERPER_API_KEY}"

    response = requests.get(url)

    for article in response.json()["news"]:
        if "title" not in article or "source" not in article or "date" not in article:
            continue
        
        headline = Headline(
            title=article["title"],
            source=article["source"],
            snippet=article.get("snippet", None),
            date=article["date"],
        )
        interest.headlines.append(headline)


if __name__ == "__main__":
    from workflow.models import Interest
    
    interests = [
        Interest("startups")
    ]
    
    for interest in interests:
        get_interest_headlines(interest)
        print(interest)