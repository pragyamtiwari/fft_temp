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

class Story(BaseModel):
    heading: str
    subheading: str
    whats_happening: str
    whats_the_context: str
    why_it_matters: str
    whats_next: str
    tldr: str

    def __str__(self):
        return (
            f"## {self.heading}\n\n"
            f"### {self.subheading}\n\n"
            f"### What's happening: {self.whats_happening}\n\n"
            f"### What's the context: {self.whats_the_context}\n\n"
            f"### Why it matters: {self.why_it_matters}\n\n"
            f"### What's next: {self.whats_next}\n\n"
            f"### TL;DR: {self.tldr}\n\n"
        )

def write_story(interest):
    # interest = user.interest
    headline = interest.selected_headline

    response = client.chat.completions.parse(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": f"You will be given a research for a news story in {interest.name}. You must write a comprehensive story that includes the following sections: 1) Heading, 2) Subheading, 3) What's happening, 4) What's the context, 5) Why it matters, 6) What's next, and 7) TL;DR. Main sections should be around four short, simple sentences. Heading and subheading should be concise and 1 sentence each. That said, you are free to modify these length suggestions if you feel a certain topic does not warrant enough detail and your writing would be trite and repetitve. That said, you cannot entirely omit any of the sections. You are writing for a sophisticated American audience that is aware of current affairs so, while you should not use needless jargon, use necessary details such as names of people, places, organizations, events, bills, etc. You must remain unbiased and qualify any statements that could be interpreted as opinion or speculation. You must not include any sources though you must rely on the given research. You should maintain and objective, BBC-like neutrality in your writing and express cautious skepticism about grand claims."},
            {
                "role": "user",
                "content": f"Research: {headline.research}",
            },
        ],
        response_format=Story,
    )
    
    interest.selected_headline.story = response.choices[0].message.parsed

if __name__ == "__main__":
    from models import User

    user = User("James", ["Startups", "World politics", "Indian politics"])
    from nodes.get_interest_headlines import get_interest_headlines
    from nodes.select_interest_headline import select_interest_headline
    from nodes.research_headline import research_headline
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
    research_headline(user)
    print("*********************************")
    print("\n\n\n\n\n")
    write_story(user)
    print("*********************************")
    print("*********************************")
    print("*********************************")
    print("******* Story *******")
    print(user.interest.selected_headline.story)
    print("*********************************")
    print("*********************************")
    print("*********************************")
    print("\n\n\n\n\n")
