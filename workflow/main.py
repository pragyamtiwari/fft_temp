from workflow.models import User
from workflow.cache import explored_interest_stories

from workflow.nodes.get_interest_headlines import get_interest_headlines
from workflow.nodes.select_interest_headline import select_interest_headline
from workflow.nodes.research_headline import research_headline
from workflow.nodes.write_story import write_story
from workflow.nodes.get_weather import get_weather
from workflow.models import Interest

import time
import random

users = [
    User(name="Pragyam", zip_code="90001", interest_names=["Business", "Pakistani politics"])
]

hm = {

}


forecasts = {}

for user in users:
    for interest in user.interests:
        if interest.name not in explored_interest_stories:
            interest = Interest(name=interest.name, previously_selected_headline_titles={hm[interest.name]} if interest.name in hm else set())
            get_interest_headlines(interest)
            select_interest_headline(interest)
            if interest.selected_headline_index is None:
                explored_interest_stories[interest.name] = "Placeholder for skipped interest story"
                print("*******************************")
                print("******* SKIPPED STORY *********")
                print("*******************************")
                continue
            research_headline(interest)
            write_story(interest)
            explored_interest_stories[interest.name] = str(interest.selected_headline.story)
            print(interest.name, str(interest.selected_headline.story))
            print(f"Finished processing interest: {interest.name}")
    if user.zip_code not in forecasts:
        forecasts[user.zip_code] = get_weather(user.zip_code)


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
            {forecasts[user.zip_code]}
        </div>
        <div style="padding: 10px;">
            <h2 style="font-size: 20px; font-weight: bold; color: #333; margin-bottom: 15px; border-bottom: 1px solid #ddd; padding-bottom: 5px; font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;">Here are your top stories for today.</h2>
"""
    res = [intro]
    # res = [f"### Good morning, {user.name}.\n", forecasts[user.zip_code], "#### Here are your top stories for today.\n"]
    random.shuffle(user.interests)
    for interest in user.interests:
        res.append(explored_interest_stories[interest.name])
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
    with open(f"{user.name}.html", "w") as f:
        f.write('\n'.join(res))
    




