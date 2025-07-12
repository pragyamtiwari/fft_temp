import os
from dotenv import load_dotenv
load_dotenv()

from linkup import LinkupClient
from exa_py import Exa
from workflow.models import Interest, Headline

client = LinkupClient(api_key=os.getenv("LINKUP_API_KEY"))

def research_headline_linkup(interest, prompt):
    response = client.search(
        query=prompt,
        depth="deep",
        output_type="sourcedAnswer",
        include_images=False,
    )

    interest.selected_headline.research = [response.answer]

    for source in response.sources:
        interest.selected_headline.research.append(f"{source.name} - {source.snippet}")

def research_headline_exa(interest, prompt):
    exa = Exa(api_key=os.getenv("EXA_API_KEY"))

    result = exa.search_and_contents(
  prompt,
  text = True,
  type = "neural"
)

    for source in result.results:
        interest.selected_headline.research.append(f"{source.title} - {source.text}")

def research_headline(interest):
    prompt = f"Please provide deep research (what's happening, why it matters, what's the context, future implications, broader trends) for the following headline: {interest.selected_headline.title}. Please write a detailed, comprehensive answer that includes mostly factual information and some reasonable analysis and sepculation. Use relevant, reliable sources. Though you should focus on context and future impliciations, the main focus is the new news which is {interest.selected_headline.title}. Please focus on the last day's news and minimize historical context."
    research_headline_exa(interest, prompt)
    

if __name__ == "__main__":
    interest = Interest("United States politics")
    interest.headlines = [Headline(
        title="Trump announces steep tariffs on 14 countries starting Aug. 1",
        source="Doesn't matter",
        snippet="Doesn't matter",
        date="Doesn't matter",
    )]
    interest.selected_headline_index = 0
    research_headline(interest)
    print(interest.selected_headline.research)
    