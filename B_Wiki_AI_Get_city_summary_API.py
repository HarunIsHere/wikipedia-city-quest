import json
import os
import random
import re
import textwrap

import wikipedia


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_LIST_FILE = os.path.join(BASE_DIR, "city_list.json")
SUMMARIES_FILE = os.path.join(BASE_DIR, "wiki_city_summaries.json")


def fetch_and_mask_city_summary(city_name):
    """Fetch and mask a short Wikipedia summary for a city."""
    try:
        summary = wikipedia.summary(
            city_name,
            sentences=random.choice([2, 3]),
        )
    except wikipedia.exceptions.DisambiguationError:
        return "No summary found for this city."
    except wikipedia.exceptions.PageError:
        return "No summary found for this city."
    except Exception as error:
        return f"Error retrieving summary: {error}"

    summary_masked = re.sub(
        rf"\b{re.escape(city_name)}\b",
        "*****",
        summary,
        flags=re.IGNORECASE,
    )
    summary_masked = re.sub(r"\([^)]*\)", "*****", summary_masked)

    return textwrap.fill(summary_masked.strip(), width=80)


def build_city_summaries():
    """Generate and save Wikipedia summaries for all cities."""
    with open(CITY_LIST_FILE, "r", encoding="utf-8") as file:
        city_list = json.load(file)

    summaries = {}

    for city in city_list:
        print(f"Fetching summary for {city} ...")
        summaries[city] = fetch_and_mask_city_summary(city)

    with open(SUMMARIES_FILE, "w", encoding="utf-8") as file:
        json.dump(summaries, file, ensure_ascii=False, indent=2)

    print("\n✅ Saved all summaries to wiki_city_summaries.json")


def load_city_summaries():
    """Load pre-generated city summaries from disk."""
    with open(SUMMARIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_city_summary(city_name):
    """Return and print a formatted city hint."""
    hint_intros = [
        "Hint:",
        "Here's a clue:",
        "Interesting fact:",
        "Did you know?",
        "Think about this place:",
    ]
    intro = random.choice(hint_intros)

    try:
        city_summaries = load_city_summaries()
        summary = city_summaries.get(
            city_name,
            "No summary available for this city.",
        )
    except FileNotFoundError:
        summary = fetch_and_mask_city_summary(city_name)

    summary_wrapped = textwrap.fill(summary, width=80)
    formatted_hint = f"{intro} {summary_wrapped}"

    print(f"\n💡 {formatted_hint}\n")
    return formatted_hint


if __name__ == "__main__":
    build_city_summaries()
