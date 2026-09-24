import requests
import json
from datetime import datetime, timezone

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

response = requests.get(TOP_STORIES_URL, timeout=10)
response.raise_for_status()

story_ids = response.json()

print("Number of top-story IDs:", len(story_ids))
print("First 5 IDs:", story_ids[:5])

story_id = story_ids[0]

response = requests.get(
    ITEM_URL.format(story_id),
    timeout=10
)

response.raise_for_status()

story = response.json()

print("Story ID:", story.get("id"))
print("Title:", story.get("title"))
print("Score:", story.get("score"))
print("Comments:", story.get("descendants", 0))
print("Author:", story.get("by"))

CATEGORY_KEYWORDS = {
    "technology": [
        "ai", "artificial intelligence", "software",
        "computer", "programming", "developer",
        "technology", "tech", "github", "google",
        "microsoft", "apple", "open source", "linux",
        "python", "javascript", "database", "cloud"
    ],

    "worldnews": [
        "war", "election", "government", "president",
        "country", "minister", "politics", "political",
        "ukraine", "russia", "china", "india",
        "israel", "gaza", "europe", "us"
    ],

    "sports": [
        "football", "soccer", "cricket", "tennis",
        "basketball", "baseball", "sports", "olympics",
        "fifa", "nfl", "nba", "premier league"
    ],

    "science": [
        "science", "scientist", "research",
        "nasa", "space", "physics", "biology",
        "chemistry", "climate", "earth",
        "astronomy", "study", "scientific"
    ],

    "entertainment": [
        "movie", "film", "music", "actor",
        "actress", "television", "tv", "show",
        "netflix", "game", "gaming", "hollywood"
    ]
}
def match_category(title):
    title = str(title).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in title for keyword in keywords):
            return category

    return None

print(match_category("NASA announces a new space mission"))
print(match_category("New AI software improves programming"))
print(match_category("India wins cricket match"))

stories = []

category_counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

for story_id in story_ids[:500]:

    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            timeout=10
        )

        response.raise_for_status()

        story = response.json()

    except requests.RequestException as e:
        print(f"Failed to fetch story {story_id}: {e}")
        continue

    title = story.get("title")

    if not title:
        continue

    category = match_category(title)

    if category is None:
        continue

    if category_counts[category] >= 25:
        continue

    record = {
        "post_id": story.get("id"),
        "title": title,
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now(timezone.utc).isoformat()
    }

    stories.append(record)

    category_counts[category] += 1

    print("\nCategory counts:")

    for category, count in category_counts.items():
         print(category, ":", count)

    print("\nTotal stories collected:", len(stories))

import os

os.makedirs("data", exist_ok=True)

date_string = datetime.now().strftime("%Y%m%d")

output_file = f"data/trends_{date_string}.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2, ensure_ascii=False)

print(f"\nSaved data to: {output_file}")