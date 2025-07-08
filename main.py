from models import User
from cache import explored_interest_stories

from nodes.get_interest_headlines import get_interest_headlines
from nodes.select_interest_headline import select_interest_headline
from nodes.research_headline import research_headline
from nodes.write_story import write_story
from nodes.get_weather import get_weather
from models import Interest

import time

users = [
    User(name="Pragyam", zip_code="10016", interest_names=["Indian politics", "United States politics", "Startups", "World politics"])
]

hm = {
    "Indian politics": "Vice President Jagdeep Dhankar opposes 'secular' in constitution.",
    "United States politics": "Elon Musk launches new political party after Trump feud",
    "World politics": "Iran leaves IAEA."
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
            print(f"Finished processing interest: {interest.name}")
    if user.zip_code not in forecasts:
        forecasts[user.zip_code] = get_weather(user.zip_code)


for user in users:
    res = [f"### Good morning, {user.name}.\n", forecasts[user.zip_code], "#### Here are your top stories for today.\n"]
    for interest in user.interests:
        res.append(explored_interest_stories[interest.name])
    res.append("### Thank you for reading.")
    with open(f"{user.name}.md", "w") as f:
        f.write('\n'.join(res))



