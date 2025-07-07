import os
from dotenv import load_dotenv
load_dotenv()

from linkup import LinkupClient

client = LinkupClient(api_key=os.getenv("LINKUP_API_KEY"))

def research_headline(interest):
    # interest = user.interest
    headline = interest.selected_headline
    snippet = headline.snippet if headline.snippet else ""

    response = client.search(
        query=f"Please provide deep research (what's happening, why it matters, what's the context, future implications, broader trends) for the following headline: {headline} {snippet}. Please write a detailed, comprehensive answer that includes mostly factual information and some reasonable analysis and sepculation.",
        depth="deep",
        output_type="sourcedAnswer",
        include_images=False,
    )

    interest.selected_headline.research = response.answer

if __name__ == "__main__":
    from models import User

    user = User("James", ["United States politics", "World politics", "Football"])
    from nodes.get_interest_headlines import get_interest_headlines
    from nodes.select_interest_headline import select_interest_headline
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
    research_headline(user)
    print("*********************************")
    print("*********************************")
    print("*********************************")
    print("******* Research *******")
    print(user.interest.selected_headline.research)
    print("*********************************")
    print("*********************************")
    print("*********************************")
    print("\n\n\n\n\n")