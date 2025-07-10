from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class SelectedHeadlineDetails(BaseModel):
    headline_index: Optional[int]
    reasoning: str

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def select_interest_headline(interest):

    system_prompt = f"""You will be given a list of recent news headlines for the topic of {interest.name}. Your task is to identify the most "suitable" headline from the list.
    
    A headline is suitable based on the following characteristics: newsworthiness, impact, engagement-inducing, novelty, objectivity, source reputation, and, most importantly, journalistic value. Weigh these characteristics carefully and make a decision about the most suitable headline. You should also note that if a subject matter comes up in many headlines from different sources, it is likely important and you may select the best of them. That said, it is possible that a bad headline is repeated many times and you should not select it. Use your best judgement to make this decision.

    After you analyze each headline, choose the most suitable headline and return its 1-based index. Additionally, provide a short reasoning behind your decision.

    That said, it is possible that no headlines are sufficiently suitable. This is common when the topic itself is not typically newsworthy. In that case, you can return None for the headline index and a short reasoning behind your decision. Sometimes, it is preferable to not select any headline if all are unsuitable and sometimes it is preferable to choose the best of the bad. You must make this decision based on the context of the topic and the availability of headlines.

    You must exclude any headlines that are sensationalist, biased, opinionated, or otherwise not journalistic in nature. This include listicles, stock reccomendations, and other low-quality content. 

    You should also exclude any headlines that cover the topics in the exclude list: {list(interest.previously_selected_headline_titles)}. If the list is empty or does not exist, you may entirely disregard this condition. The headlines in the exclude list were selected in previous iterations and re-selection may be repetitive for the reader. That said, if there are important updates to the topic, you may select a headline despite it being related to an element on the exclude list.

    Do not select overly-academic headlines or low-quality content. Interesting, engaging, novel, and entertaining headlines are preferred, but since this is a subjective matter, you must exercise your best judgement. You must ask yourself the question whether the headline you select would be of interest to a sophisticated, millennial American audience and worthy of publication on a major news website. Remeber to focus on factual current information rather than broad essays.
    """

    response = client.chat.completions.parse(

    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": str(interest),
        },
    ],
    response_format=SelectedHeadlineDetails,
)
    parsed_response = response.choices[0].message.parsed
    print(f"Reasoning: {parsed_response.reasoning}")

    interest.selected_headline_index = parsed_response.headline_index - 1 if parsed_response.headline_index is not None else None

if __name__ == "__main__":
    from workflow.nodes.get_interest_headlines import get_interest_headlines
    from workflow.models import Interest
    
    interests = []

    test_interest_names = ["United States politics", "Indian politics", "Pakistani politics", "Soccer", "Technology", "Startups", "Cricket", "Hollywood", "World Affairs", "Artificial intelligence"]

    for interest_name in test_interest_names:
        interests.append(Interest(interest_name))

    
    for interest in interests:
        print(f"Processing interest: {interest.name}")
        get_interest_headlines(interest)
        select_interest_headline(interest)
        print(interest.selected_headline.title)
        print(interest.selected_headline.source)
        print("\n\n\n\n")
        