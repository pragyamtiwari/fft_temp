from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class SelectedHeadlineDetails(BaseModel):
    any_interesting_headline: bool
    headline_index: Optional[int]

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def select_interest_headline(interest):
    # interest = user.interest
    print(interest.name)

    response = client.chat.completions.parse(

    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": f"You will be given a list of headlines for the topic of {interest.name}, you must decide two things. 1) Whether or not there exists at least one headline that is interesting and impactful. If such a headline exists, you should populate any_interesting_headline with True. If no such headline exists, you should populate any_interesting_headline with False. 2) If any_interesting_headline is True, you must also populate headline_index with the 1-based index of the most interesting headline in the list. If any_interesting_headline is False, you should populate headline_index with None. You must disregard any news older than 1 week. Additionally, do not select any headlines covering the same topics that are in the exclude list since they have already been explored in a previous iteration. Exclude list: {str(interest.previously_selected_headline_titles)}. Do note the two exceptions: 1) If the list is empty or does not exist, you may entirely disregard it. 2) If the new headline contains new, significant information and was recrently published (less than 24 hours ago), you may select it."},
        {
            "role": "user",
            "content": str(interest),
        },
    ],
    response_format=SelectedHeadlineDetails,
)
    parsed_response = response.choices[0].message.parsed
    
    if parsed_response.any_interesting_headline:
        interest.selected_headline_index = parsed_response.headline_index - 1
    else:
        interest.selected_headline_index = None

if __name__ == "__main__":
    from models import User

    user = User("James", ["United States politics", "World politics", "Football"])
    from nodes.get_interest_headlines import get_interest_headlines
    for i in range(len(user.interests)):
        user.interest_index = i
        if i == 0:
            user.interest.previously_selected_headline_titles.add("Elon Musk starts new political party, America, after conflict with Trump")
        get_interest_headlines(user)
        print(user.interest)
        select_interest_headline(user)
        print("*********************************")
        print("*********************************")
        print("*********************************")
        print("******* Selected Headline *******")
        print(user.interest.selected_headline)
        print("*********************************")
        print("*********************************")
        print("*********************************")
        print("\n\n\n\n\n")
