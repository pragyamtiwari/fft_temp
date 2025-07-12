from workflow.models import User
from workflow.cache import explored_interest_stories

from workflow.nodes.get_interest_headlines import get_interest_headlines
from workflow.nodes.select_interest_headline import select_interest_headline
from workflow.nodes.research_headline import research_headline
from workflow.nodes.write_story import write_story
from workflow.nodes.get_weather import get_weather
from workflow.models import Interest
from workflow.nodes.send_story import send_story

import os
from dotenv import load_dotenv
load_dotenv()

from upstash_redis import Redis

r = Redis(url="https://saving-rat-52046.upstash.io", token=os.getenv("UPSTASH_REDIS_TOKEN"))


import time
import random

users = [
    User(email="pragyam.tiwari@gmail.com", name="Pragyam", zip_code="10018", interest_names=["soccer", "economy", "finance", "startups"])
]

hm = {

}


forecasts = {}

for user in users:
    for interest in user.interests:
        if r.get(interest.name) is None:
            interest = Interest(name=interest.name)
            get_interest_headlines(interest)
            print("Interest Headlines:")
            print(interest)
            print("Selected Headline:")
            select_interest_headline(interest)
            if interest.selected_headline_index is None:
                explored_interest_stories[interest.name] = "Placeholder for skipped interest story"
                print("*******************************")
                print("******* SKIPPED STORY *********")
                print("*******************************")
                continue
            print(interest.selected_headline)
            print("\n\n\n\n")
        
            research_headline(interest)
            write_story(interest)
            r.set(interest.name, str(interest.selected_headline.story))
            print(interest.name, str(interest.selected_headline.story))
            print(f"Finished processing interest: {interest.name}")
    if r.get(user.zip_code) is None:
        r.set(user.zip_code, get_weather(user.zip_code))


for user in users:
    intro = f"""
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 5px; background-color: #ffffff;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white;">
        <div style="background-color: #f5f5f5; padding: 10px; border-bottom: 1px solid #ddd;">
            <h1 style="font-size: 24px; font-weight: normal; margin: 0 0 12px 0; color: #333; font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;">Good morning, {user.name}.</h1>
            {r.get(user.zip_code)}
        </div>
        <div style="padding: 10px;">
            <h2 style="font-size: 20px; font-weight: bold; color: #333; margin-bottom: 15px; border-bottom: 1px solid #ddd; padding-bottom: 5px; font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;">Here are your top stories for today.</h2>
"""
    res = [intro]
    random.shuffle(user.interests)
    for interest in user.interests:
        res.append(r.get(interest.name))
    conclusion = """
        </div>
        <div style="background-color: #f5f5f5; text-align: center; padding: 8px; font-size: 17px; border-top: 1px solid #ddd; color: #666; font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;">
            Thank you for reading.
        </div>
    </div>
</body>
</html>
"""
    res.append(conclusion)
    send_story(user.email, '\n'.join(res))
    with open(f"{user.name}.html", "w") as f:
        f.write('\n'.join(res))

r.flushdb()
    