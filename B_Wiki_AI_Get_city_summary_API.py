import wikipedia
import re
import random
import json
import textwrap
# import G_Similarity_Match_for_WikisAPI

def get_city_summary(city_name):
    try:
        summary = wikipedia.summary(city_name, sentences=random.choice([2, 3]))
    except wikipedia.exceptions.DisambiguationError as e:
        return "No summary found for this city."
        # return G_Similarity_Match_for_WikisAPI.custom_get_close_matches(city_name, e, n=1, cutoff=0.9)
    except wikipedia.exceptions.PageError:
        return "No summary found for this city."
    except Exception as e:
        return f"Error retrieving summary: {e}"

    summary_masked = re.sub(rf'\b{re.escape(city_name)}\b', '*****', summary, flags=re.IGNORECASE)
    summary_masked = re.sub(r'\([^)]*\)', '*****', summary_masked)
    new_summary_masked = textwrap.fill(summary_masked, width=80)
    return new_summary_masked.strip()

# Load your city list
with open("city_list.json", "r") as f:
    city_list = json.load(f)

summaries = {}
for city in city_list:
    print(f"Fetching summary for {city} ...")
    summaries[city] = get_city_summary(city)

# Save to JSON
with open("wiki_city_summaries.json", "w", encoding="utf-8") as f:
    json.dump(summaries, f, ensure_ascii=False, indent=2)

print("\n✅ Saved all summaries to wiki_city_summaries.json")



with open("wiki_city_summaries.json", "r", encoding="utf-8") as f:
    city_summaries = json.load(f)


def get_city_summary(city_name):
    hint_intros = [
        "Hint:",
        "Here's a clue:",
        "Interesting fact:",
        "Did you know?",
        "Think about this place:"
    ]
    intro = random.choice(hint_intros)
    summary = city_summaries.get(city_name, "No summary available for this city.")
    summary_new = textwrap.fill(summary, width=80)
    formatted_hint = f"{intro} {summary_new}"
    print(f"\n💡 {formatted_hint}\n")
    return formatted_hint



# import wikipedia
# import re
# import random
# import json
#
# def get_city_summary(city_name):
#     """
#     Fetches a short, masked Wikipedia summary for the given city.
#     Replaces:
#       • The city name with '*****'
#       • Anything inside parentheses (...) with asterisks
#     Adds minor randomization to the hint phrasing.
#     """
#
#     try:
#         summary = wikipedia.summary(city_name, sentences=random.choice([2, 3]))
#     except wikipedia.exceptions.DisambiguationError as e:
#         summary = wikipedia.summary(e.options[0], sentences=2)
#     except wikipedia.exceptions.PageError:
#         return "No summary found for this city."
#     except Exception as e:
#         return f"Error retrieving summary: {e}"
#
#     # Mask the city name (case-insensitive, whole word)
#     summary_masked = re.sub(rf'\b{re.escape(city_name)}\b', '*****', summary, flags=re.IGNORECASE)
#
#     # Replace contents inside parentheses with stars
#     summary_masked = re.sub(r'\([^)]*\)', '*****', summary_masked)
#
#     # Add random intro style
#     hint_intros = [
#         "Hint:",
#         "Here's a clue:",
#         "Interesting fact:",
#         "Did you know?",
#         "Think about this place:"
#     ]
#     intro = random.choice(hint_intros)
#
#     formatted_hint = f"{intro} {summary_masked.strip()}"
#
#     print(f"\n💡 {formatted_hint}\n")
#     return formatted_hint





# def save_to_json(data, filename=OUTPUT_FILE):
#     for info in data.values():
#         if info.get("population") is not None:
#             info["population"] = f"{info['population']:,}"
#
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, ensure_ascii=False)



# import wikipedia
# import re
# import random
#
#
# def get_city_summary(city_name):
#     """
#     Fetches a short, masked Wikipedia summary for the given city.
#     If the city name appears in the summary, it’s replaced with '*'.
#     Adds minor randomization in how the hint is phrased.
#     """
#
#     try:
#         # Get 2–3 sentences for richer hints
#         summary = wikipedia.summary(city_name, sentences=random.choice([2, 3]))
#     except wikipedia.exceptions.DisambiguationError as e:
#         # Choose the most relevant option automatically
#         summary = wikipedia.summary(e.options[0], sentences=2)
#     except wikipedia.exceptions.PageError:
#         return "No summary found for this city."
#     except Exception as e:
#         return f"Error retrieving summary: {e}"
#
#     # Mask all case variants of the city name (whole words only)
#     pattern = re.compile(rf'\b{re.escape(city_name)}\b', re.IGNORECASE)
#     summary_masked = pattern.sub('*****', summary)
#
#     # Optional: add some variation in the hint style
#     hint_intros = [
#         "Hint:",
#         "Here's a clue:",
#         "Interesting fact:",
#         "Did you know?",
#         "Think about this place:"
#     ]
#     intro = random.choice(hint_intros)
#
#     formatted_hint = f"{intro} {summary_masked}"
#
#     print(f"\n💡 {formatted_hint}\n")
#     return formatted_hint
#





# import wikipedia
# import re
#
#
# def get_city_summary(city_name):
#     """
#     Fetches a short summary for the given city from Wikipedia.
#     Removes IPA/pronunciation text, replaces the city name with '*',
#     and returns a clean hint string.
#     """
#
#     try:
#         summary = wikipedia.summary(city_name, sentences=2)
#     except wikipedia.exceptions.DisambiguationError as e:
#         summary = wikipedia.summary(e.options[0], sentences=2)
#     except wikipedia.exceptions.PageError:
#         return "No summary found for this city."
#     except Exception as e:
#         return f"Error retrieving summary: {e}"
#
#     # Remove IPA / pronunciation text (e.g. (BAR-sə-LOH-nə; Catalan: ...))
#     summary = re.sub(r'\([^)]*[ˈˌʃʒθəɾɲɡa-zA-Z;:\[\]]*[^)]*\)', '', summary)
#
#     # Replace the city name (case-insensitive, whole words only)
#     pattern = re.compile(rf'\b{re.escape(city_name)}\b', re.IGNORECASE)
#     summary_masked = pattern.sub('*', summary)
#
#     # Clean double spaces and trailing spaces
#     summary_masked = re.sub(r'\s+', ' ', summary_masked).strip()
#
#     # Return neatly formatted text (no auto-print)
#     return f"💡 Hint: {summary_masked}"

# import wikipedia
# import re
# import random
#
#
# def get_city_summary(city_name):
#     """
#     Fetches a short, masked Wikipedia summary for the given city.
#     Removes pronunciation/IPA text and returns a readable one-line hint.
#     If nothing usable remains, returns a default message.
#     """
#
#     try:
#         summary = wikipedia.summary(city_name, sentences=random.choice([2, 3]))
#     except wikipedia.exceptions.DisambiguationError as e:
#         summary = wikipedia.summary(e.options[0], sentences=2)
#     except wikipedia.exceptions.PageError:
#         return "No summary found for this city."
#     except Exception:
#         return "Could not fetch Wikipedia info right now."
#
#     # Remove pronunciation/IPA parts like "(BAR-sə-LOH-nə; Catalan: ...)"
#     summary = re.sub(r'\([^)]*[ˈˌʃʒθəɾɲɡa-zA-Z;:\[\]]*[^)]*\)', '', summary)
#
#     # Mask city name
#     pattern = re.compile(rf'\b{re.escape(city_name)}\b', re.IGNORECASE)
#     summary_masked = pattern.sub('*', summary)
#
#     # Clean extra whitespace
#     summary_masked = re.sub(r'\s+', ' ', summary_masked).strip()
#
#     # If everything was stripped, give a backup hint
#     if not summary_masked or len(summary_masked) < 40:
#         return f"Think of a major landmark or region related to {city_name}."
#
#     # Add variety
#     intro = random.choice([
#         "Hint:",
#         "Interesting fact:",
#         "Here's a clue:",
#         "Think about this place:"
#     ])
#
#     return f"💡 {intro} {summary_masked}"





# import wikipedia
#
#
# def get_city_summary(city_name):
#     """
#     Fetches a short summary for the given city from Wikipedia.
#     If the city name appears in the summary, it is replaced with '*'.
#     """
#
#     try:
#         summary = wikipedia.summary(city_name, sentences=2)
#     except wikipedia.exceptions.DisambiguationError as e:
#         # Choose the first option if there are multiple pages
#         summary = wikipedia.summary(e.options[0], sentences=2)
#     except wikipedia.exceptions.PageError:
#         summary = "No summary found for this city."
#     except Exception as e:
#         summary = f"Error retrieving summary: {e}"
#
#     # Replace occurrences of the city name (case-insensitive) with '*'
#     summary_masked = summary.replace(city_name, "*").replace(city_name.lower(), "*").replace(city_name.upper(), "*")
#
#     print(f"📖 {summary_masked}\n")
#     return summary_masked