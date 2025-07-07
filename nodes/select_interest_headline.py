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
    reasoning: str

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def select_interest_headline(interest):
    # interest = user.interest
    print(interest.name)
    print(f"You will be given a list of headlines for the topic of {interest.name}, you must decide two things. 1) Whether or not there exists at least one headline that is interesting and impactful. If such a headline exists, you should populate any_interesting_headline with True. If no such headline exists, you should populate any_interesting_headline with False. 2) If any_interesting_headline is True, you must also populate headline_index with the 1-based index of the most interesting headline in the list. If any_interesting_headline is False, you should populate headline_index with None. You must disregard any news older than 1 week. Additionally, do not select any headlines covering the same topics that are in the exclude list since they have already been explored in a previous iteration. Exclude list: {str(interest.previously_selected_headline_titles)}. Do note the two exceptions: 1) If the list is empty or does not exist, you may entirely disregard it. 2) If the new headline contains new, significant information and was recrently published (less than 24 hours ago), you may select it.")


    response = client.chat.completions.parse(

    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": f"You will be given a list of headlines for the topic of {interest.name}, you must decide two things. 1) Whether or not there exists at least one headline that is interesting and impactful. If such a headline exists, you should populate any_interesting_headline with True. If no such headline exists, you should populate any_interesting_headline with False. 2) If any_interesting_headline is True, you must also populate headline_index with the 1-based index of the most interesting headline in the list. If any_interesting_headline is False, you should populate headline_index with None. Additionally, do not select any headlines covering the same topics that are in the exclude list since they have already been explored in a previous iteration. Exclude list: {str(interest.previously_selected_headline_titles)}. Do note the two exceptions: 1) If the list is empty or does not exist, you may entirely disregard it. 2) If the new headline contains new, significant information, you may select it."},
        {
            "role": "user",
            "content": str(interest),
        },
    ],
    response_format=SelectedHeadlineDetails,
)
    parsed_response = response.choices[0].message.parsed
    print(parsed_response)
    
    if parsed_response.any_interesting_headline:
        interest.selected_headline_index = parsed_response.headline_index - 1
    else:
        interest.selected_headline_index = None

if __name__ == "__main__":
    from nodes.get_interest_headlines import get_interest_headlines
    from models import User, Interest
    interests = [
        Interest("United States politics", previously_selected_headline_titles=set(["Elon Musk launches new political party"])),
        Interest("World politics", previously_selected_headline_titles=set()),
        Interest("Indian politics", previously_selected_headline_titles=set(["Jagdeep Dhankar disgruntled about 'secular' and 'socialist' in Constitution"])),
        ]
    
    for interest in interests:
        print(f"Processing interest: {interest.name}")
        get_interest_headlines(interest)
        select_interest_headline(interest)
        print(interest.selected_headline)