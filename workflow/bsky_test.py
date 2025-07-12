from atproto import Client
import os
from dotenv import load_dotenv
import json
load_dotenv()

# Create client and login
client = Client()
client.login('pragyam.bsky.social', os.getenv("BSKY_APP_PASSWORD"))

# Get user's last 5 posts
handle = "hankgreen.bsky.social"
posts = client.app.bsky.feed.get_author_feed(
    params={
        "actor": handle,
        "limit": 5
    }
)

res = []

for post in posts.feed:
    print(post.post.record.text)
    if post.post.embed:
        print("Embed: ", post.post.embed.record.value.text)

print(res)

