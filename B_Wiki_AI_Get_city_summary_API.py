import json
import os
import random
import re
import textwrap

import wikipedia


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_LIST_FILE = os.path.join(BASE_DIR, "city_list.json")
CITY_INFO_FILE = os.path.join(BASE_DIR, "City_Info_API.json")
SUMMARIES_FILE = os.path.join(BASE_DIR, "wiki_city_summaries.json")


def load_city_list():
    """Load the curated list of playable cities."""
    with open(CITY_LIST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_city_info():
    """Load generated city info if available."""
    with open(CITY_INFO_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_summary(summary, city_name):
    """Mask the city name and remove parenthetical text."""
    masked_summary = re.sub(
        rf"\b{re.escape(city_name)}\b",
        "*****",
        summary,
        flags=re.IGNORECASE,
    )
    masked_summary = re.sub(r"\([^)]*\)", "*****", masked_summary)
    masked_summary = re.sub(r"\s+", " ", masked_summary).strip()
    return textwrap.fill(masked_summary, width=80)


def fetch_city_summary(city_name, country=None):
    """Fetch a safer city summary from Wikipedia using city and country."""
    queries = []

    if country:
        queries.append(f"{city_name}, {country}")

    queries.append(city_name)

    for query in queries:
        try:
            summary = wikipedia.summary(query, sentences=random.choice([2, 3]))
            return clean_summary(summary, city_name)
        except wikipedia.exceptions.DisambiguationError as error:
            for option in error.options:
                option_lower = option.lower()
                if city_name.lower() in option_lower:
                    try:
                        summary = wikipedia.summary(
                            option,
                            sentences=random.choice([2, 3]),
                        )
                        return clean_summary(summary, city_name)
                    except Exception:
                        continue
        except wikipedia.exceptions.PageError:
            continue
        except Exception:
            continue

    return "No summary found for this city."


def build_city_summaries():
    """Generate summaries for the curated playable city list."""
    city_list = load_city_list()

    try:
        city_info = load_city_info()
    except FileNotFoundError:
        city_info = {}

    summaries = {}

    for city_name in city_list:
        print(f"Fetching summary for {city_name} ...")
        country = city_info.get(city_name, {}).get("country")
        summaries[city_name] = fetch_city_summary(city_name, country)

    with open(SUMMARIES_FILE, "w", encoding="utf-8") as file:
        json.dump(summaries, file, ensure_ascii=False, indent=2)

    print("\n✅ Saved all summaries to wiki_city_summaries.json")


def load_city_summaries():
    """Load saved city summaries."""
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
        summary = fetch_city_summary(city_name)

    formatted_hint = f"{intro} {summary}"
    print(f"\n💡 {formatted_hint}\n")
    return formatted_hint


if __name__ == "__main__":
    build_city_summaries()
