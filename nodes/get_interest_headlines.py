import os
from dotenv import load_dotenv

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

import requests

from models import Headline


def get_interest_headlines(interest):
    # interest = user.interest
    interest_name_parsed = interest.name.replace(" ", "+")
    num_results = 20

    url = f"https://google.serper.dev/news?q={interest_name_parsed}&num={num_results}&apiKey={SERPER_API_KEY}"

    response = requests.get(url)
    
    count = 0

    for article in response.json()["news"]:
        headline = Headline(
            title = article["title"],
            source = article["source"],
            snippet = article.get("snippet", None),
            date = article["date"],
        )
        interest.headlines.append(headline)

if __name__ == "__main__":
    from models import User

    user = User("James", ["United States politics", "Health", "Sports"])
    get_interest_headlines(user)
    print(user.interest)




