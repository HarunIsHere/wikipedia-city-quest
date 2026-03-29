import json
import os
import time

import certifi
import requests
import wikipedia


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_LIST_FILE = os.path.join(BASE_DIR, "city_list.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "City_Info_API.json")

GEODB_HOST = "wft-geo-db.p.rapidapi.com"
GEODB_KEY = "YOUR_RAPIDAPI_KEY_HERE"
DELAY = 1

HEADERS_GEODB = {
    "X-RapidAPI-Key": GEODB_KEY,
    "X-RapidAPI-Host": GEODB_HOST,
    "Accept": "application/json",
    "User-Agent": "CityDataCollector/1.0",
}

HEADERS_WIKIDATA = {
    "User-Agent": "CityInfoFetcher/1.0 (your_email@example.com)",
}

WD_ENDPOINT = "https://query.wikidata.org/sparql"


def load_city_list():
    """Load the curated list of playable cities."""
    with open(CITY_LIST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def fetch_city_base_data(city_name):
    """Fetch one city's base data from GeoDB using the curated city name."""
    url = f"https://{GEODB_HOST}/v1/geo/cities"
    params = {
        "namePrefix": city_name,
        "limit": 10,
        "sort": "-population",
    }

    response = requests.get(
        url,
        headers=HEADERS_GEODB,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    items = response.json().get("data", [])
    if not items:
        return None

    exact_match = None
    fallback_match = None

    for item in items:
        item_city = (item.get("city") or "").strip()
        item_name = (item.get("name") or "").strip()

        if item_city.lower() == city_name.lower():
            exact_match = item
            break

        if item_name.lower() == city_name.lower():
            exact_match = item
            break

        if fallback_match is None:
            fallback_match = item

    selected = exact_match or fallback_match
    if selected is None:
        return None

    return {
        "city": selected.get("city") or city_name,
        "country": selected.get("country"),
        "country_code": selected.get("countryCode"),
        "population": selected.get("population"),
        "latitude": selected.get("latitude"),
        "longitude": selected.get("longitude"),
        "region": selected.get("region"),
        "id": selected.get("id"),
        "wikiDataId": selected.get("wikiDataId"),
        "continent": None,
        "wikiDataURL": None,
        "summary": None,
        "languages": [],
        "currencies": [],
        "timezones": [],
        "image_url": None,
    }


def query_wikidata(qid):
    """Query Wikidata for selected city attributes."""
    query = f"""
    SELECT ?cityLabel ?continentLabel ?officialLanguageLabel
           ?area ?osmId ?filmLabel ?officialSymbolLabel
           ?sharesBorderWithLabel ?geoShape ?coordinateLocation
           ?timeZoneLabel ?nextToWaterLabel ?physicalFeatureLabel
    WHERE {{
      OPTIONAL {{ wd:{qid} rdfs:label ?cityLabel FILTER(LANG(?cityLabel) = "en") }}
      OPTIONAL {{ wd:{qid} wdt:P30 ?continent. }}
      OPTIONAL {{ wd:{qid} wdt:P37 ?officialLanguage. }}
      OPTIONAL {{ wd:{qid} wdt:P2046 ?area. }}
      OPTIONAL {{ wd:{qid} wdt:P402 ?osmId. }}
      OPTIONAL {{ wd:{qid} wdt:P31 ?film. }}
      OPTIONAL {{ wd:{qid} wdt:P41 ?officialSymbol. }}
      OPTIONAL {{ wd:{qid} wdt:P47 ?sharesBorderWith. }}
      OPTIONAL {{ wd:{qid} wdt:P3896 ?geoShape. }}
      OPTIONAL {{ wd:{qid} wdt:P625 ?coordinateLocation. }}
      OPTIONAL {{ wd:{qid} wdt:P421 ?timeZone. }}
      OPTIONAL {{ wd:{qid} wdt:P206 ?nextToWater. }}
      OPTIONAL {{ wd:{qid} wdt:P706 ?physicalFeature. }}

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 1
    """

    try:
        response = requests.get(
            WD_ENDPOINT,
            params={"query": query, "format": "json"},
            headers=HEADERS_WIKIDATA,
            verify=certifi.where(),
            timeout=30,
        )
        response.raise_for_status()
        results = response.json()
        bindings = results.get("results", {}).get("bindings", [])

        if not bindings:
            return {}

        binding = bindings[0]
        data = {}

        for key, value in binding.items():
            data[key] = value.get("value")

        area_value = data.get("area")
        if area_value is not None:
            try:
                data["area_km2"] = round(float(area_value), 2)
            except (TypeError, ValueError):
                data["area_km2"] = None
        else:
            data["area_km2"] = None

        coordinate_value = data.get("coordinateLocation")
        if coordinate_value and coordinate_value.startswith("Point("):
            try:
                lon, lat = map(
                    float,
                    coordinate_value.replace("Point(", "").replace(")", "").split(),
                )
                data["coordinateLocation"] = {"lat": lat, "lon": lon}
            except (TypeError, ValueError):
                data["coordinateLocation"] = None

        return data

    except requests.RequestException:
        return {}


def get_city_image(images):
    """Return the most suitable city image URL from Wikipedia images."""
    banned_keywords = [
        "flag",
        "coat",
        "arms",
        "emblem",
        "seal",
        "map",
        "locator",
        "symbol",
        "logo",
        "banner",
        "blason",
        "insignia",
        "outline",
        "satellite",
        "shield",
        "diagram",
        "icon",
    ]
    preferred_ext = (".jpg", ".jpeg", ".png", ".webp")

    candidates = [
        image
        for image in images
        if image.lower().endswith(preferred_ext)
        and not any(keyword in image.lower() for keyword in banned_keywords)
    ]

    candidates.sort(
        key=lambda image: (
            "skyline" in image.lower() or "city" in image.lower(),
            "wikimedia" in image.lower(),
            -len(image),
        ),
        reverse=True,
    )

    return candidates[0] if candidates else None


def add_wikipedia_summary_and_image(city_name, city_info):
    """Fetch city summary and image from Wikipedia."""
    country = city_info.get("country")
    query = f"{city_name}, {country}" if country else city_name

    try:
        page = wikipedia.page(query, auto_suggest=False)
        summary = wikipedia.summary(query, sentences=3, auto_suggest=False)
        city_info["summary"] = summary
        city_info["image_url"] = get_city_image(page.images)
        return city_info
    except wikipedia.exceptions.DisambiguationError as error:
        for option in error.options:
            if city_name.lower() in option.lower():
                try:
                    page = wikipedia.page(option, auto_suggest=False)
                    city_info["summary"] = wikipedia.summary(
                        option,
                        sentences=3,
                        auto_suggest=False,
                    )
                    city_info["image_url"] = get_city_image(page.images)
                    return city_info
                except Exception:
                    continue
    except wikipedia.exceptions.PageError:
        pass
    except Exception:
        pass

    city_info["summary"] = None
    city_info["image_url"] = None
    return city_info


def build_city_info():
    """Build city info only for the curated playable city list."""
    cities = load_city_list()
    city_info_data = {}

    for city_name in cities:
        print(f"Fetching data for {city_name} ...")

        try:
            base_data = fetch_city_base_data(city_name)
        except requests.RequestException as error:
            print(f"❌ Could not fetch base data for {city_name}: {error}")
            base_data = None

        if base_data is None:
            city_info_data[city_name] = {
                "city": city_name,
                "country": None,
                "country_code": None,
                "population": None,
                "latitude": None,
                "longitude": None,
                "region": None,
                "id": None,
                "wikiDataId": None,
                "continent": None,
                "wikiDataURL": None,
                "summary": None,
                "languages": [],
                "currencies": [],
                "timezones": [],
                "image_url": None,
            }
            continue

        qid = base_data.get("wikiDataId")
        if qid:
            wikidata_data = query_wikidata(qid)
            base_data.update(wikidata_data)

            if "continentLabel" in base_data:
                base_data["continent"] = base_data["continentLabel"]

            if "officialLanguageLabel" in base_data:
                base_data["languages"] = [base_data["officialLanguageLabel"]]

            if "timeZoneLabel" in base_data:
                base_data["timezones"] = [base_data["timeZoneLabel"]]

        base_data = add_wikipedia_summary_and_image(city_name, base_data)
        city_info_data[city_name] = base_data
        time.sleep(DELAY)

    return city_info_data


def save_to_json(data, filename=OUTPUT_FILE):
    """Save city info data to JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    city_info = build_city_info()
    save_to_json(city_info)
    print(f"✅ Data saved to {OUTPUT_FILE}")
