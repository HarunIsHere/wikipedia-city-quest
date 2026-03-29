import json
import random
import time
from collections import defaultdict

import certifi
import requests
import wikipedia


TOP_N = 50
LIMIT_PER_REQUEST = 10
OUTPUT_FILE = "city_info_api.json"
DELAY = 1
MAX_RETRIES = 5

GEODB_HOST = "wft-geo-db.p.rapidapi.com"
GEODB_KEY = "60b10cec3dmsh63212fbfa712c74p1cd6e7jsnb17850f361ad"

HEADERS_GEODB = {
    "X-RapidAPI-Key": GEODB_KEY,
    "X-RapidAPI-Host": GEODB_HOST,
    "Accept": "application/json",
    "User-Agent": "CityDataCollector/1.0",
}

HEADERS_WIKIDATA = {
    "User-Agent": "CityInfoFetcher/1.0 (harunayarturk@gmail.com)",
}

WD_ENDPOINT = "https://query.wikidata.org/sparql"


def fetch_top_cities(top_n=TOP_N):
    """Fetch top cities by population."""
    cities = {}
    offset = 0

    while len(cities) < top_n:
        url = f"https://{GEODB_HOST}/v1/geo/cities"
        params = {
            "sort": "-population",
            "limit": LIMIT_PER_REQUEST,
            "offset": offset,
        }

        try:
            response = requests.get(
                url,
                headers=HEADERS_GEODB,
                params=params,
                timeout=30,
            )

            if response.status_code == 429:
                print("⚠️ Processing.... please wait.")
                time.sleep(DELAY * 5)
                continue

            if response.status_code == 403:
                print("❌ Forbidden: check API key or subscription.")
                break

            response.raise_for_status()
            data = response.json()
        except requests.RequestException as error:
            print(f"❌ HTTP error fetching cities: {error}")
            break

        items = data.get("data", [])
        if not items:
            break

        for item in items:
            city_name = item.get("name")
            if city_name in cities:
                continue

            cities[city_name] = {
                "city": item.get("city"),
                "country": item.get("country"),
                "country_code": item.get("countryCode"),
                "population": item.get("population"),
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude"),
                "region": item.get("region"),
                "id": item.get("id"),
                "wikiDataId": item.get("wikiDataId"),
                "continent": None,
                "wikiDataURL": None,
                "summary": None,
                "languages": [],
                "currencies": [],
                "timezones": [],
                "image_url": None,
            }

            if len(cities) >= top_n:
                break

        offset += LIMIT_PER_REQUEST

        if len(cities) < top_n:
            time.sleep(DELAY)

    print(f"✅ Retrieved the top {len(cities)} global cities (by population).")
    return cities


def query_wikidata(qid):
    """Query Wikidata for city attributes using requests and certifi."""
    query = f"""
    SELECT ?cityLabel ?continentLabel ?officialLanguageLabel ?significantEventLabel
           ?area ?highestPoint ?aerialView ?osmId ?filmLabel ?officialSymbolLabel
           ?sharesBorderWithLabel ?geoShape ?coordinateLocation ?timeZoneLabel
           ?nextToWaterLabel ?physicalFeatureLabel
    WHERE {{
      wd:{qid} rdfs:label ?cityLabel .
      FILTER(LANG(?cityLabel) = "en")

      OPTIONAL {{ wd:{qid} wdt:P30 ?continent. }}
      OPTIONAL {{ wd:{qid} wdt:P37 ?officialLanguage. }}
      OPTIONAL {{ wd:{qid} wdt:P793 ?significantEvent. }}
      OPTIONAL {{ wd:{qid} wdt:P2046 ?area. }}
      OPTIONAL {{ wd:{qid} wdt:P610 ?highestPoint. }}
      OPTIONAL {{ wd:{qid} wdt:P18 ?aerialView. }}
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

        data = defaultdict(list)
        for key, value in bindings[0].items():
            data[key].append(value.get("value"))

        if "area" in data:
            try:
                data["area_km2"] = [float(data["area"][0]) / 1_000_000]
            except (TypeError, ValueError, IndexError):
                data["area_km2"] = None

        if "highestPoint" in data:
            try:
                data["highestPoint_m"] = [float(data["highestPoint"][0])]
            except (TypeError, ValueError, IndexError):
                data["highestPoint_m"] = None

        for key in ["filmLabel", "officialSymbolLabel"]:
            if key not in data:
                data[key] = []

        return dict(data)

    except requests.RequestException:
        return {}


def enrich_city(cities_dict):
    """Enrich city data with Wikidata information."""
    enriched = {}
    print("⚠️ Enriching city data - please wait...")

    for city_name, city_data in cities_dict.items():
        qid = city_data.get("wikiDataId")
        if not qid:
            enriched[city_name] = city_data
            continue

        wikidata_info = query_wikidata(qid)

        for key in [
            "continentLabel",
            "highestPoint_m",
            "area_km2",
            "osmId",
            "coordinateLocation",
            "timeZoneLabel",
        ]:
            if key in wikidata_info and wikidata_info[key]:
                wikidata_info[key] = wikidata_info[key][0]

        if (
            "coordinateLocation" in wikidata_info
            and wikidata_info["coordinateLocation"]
        ):
            coord = wikidata_info["coordinateLocation"]
            if coord.startswith("Point(") and coord.endswith(")"):
                try:
                    lon, lat = map(
                        float,
                        coord.replace("Point(", "").replace(")", "").split(),
                    )
                    wikidata_info["coordinateLocation"] = {
                        "lat": lat,
                        "lon": lon,
                    }
                except (TypeError, ValueError):
                    wikidata_info["coordinateLocation"] = None

        for list_key in ["filmLabel", "officialSymbolLabel"]:
            if list_key not in wikidata_info:
                wikidata_info[list_key] = []

        city_data.update(wikidata_info)
        enriched[city_name] = city_data

    return enriched


def add_wikipedia_summary_and_image(cities):
    """Add Wikipedia summary and image URL to each city."""
    for city_name, info in cities.items():
        country = info.get("country")
        query = f"{city_name}, {country}" if country else city_name

        try:
            page = wikipedia.page(query, auto_suggest=False)
            summary = wikipedia.summary(query, sentences=3, auto_suggest=False)

            image_url = get_city_image(page.images)
            info["summary"] = summary
            info["image_url"] = image_url

        except wikipedia.exceptions.DisambiguationError as error:
            options = [
                option
                for option in error.options
                if "city" in option.lower() or "capital" in option.lower()
            ]
            if options:
                try:
                    page = wikipedia.page(options[0], auto_suggest=False)
                    summary = " ".join(page.summary.split(". ")[:3])
                    image_url = get_city_image(page.images)
                    info["summary"] = summary
                    info["image_url"] = image_url
                except Exception:
                    info["summary"] = None
                    info["image_url"] = None
            else:
                info["summary"] = None
                info["image_url"] = None

        except wikipedia.exceptions.PageError:
            info["summary"] = None
            info["image_url"] = None

        except Exception:
            info["summary"] = None
            info["image_url"] = None

        time.sleep(random.uniform(0.5, 1.5))

    print("✅ Added Wikipedia summaries")
    return cities


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
    ]
    preferred_ext = (".jpg", ".jpeg", ".png", ".webp")

    candidates = [
        image
        for image in images
        if image.lower().endswith(preferred_ext)
        and not any(bad in image.lower() for bad in banned_keywords)
    ]

    candidates.sort(
        key=lambda image: (
            "skyline" in image.lower() or "city" in image.lower(),
            "wikimedia" in image.lower(),
            len(image),
        ),
        reverse=True,
    )

    return candidates[0] if candidates else None


def save_to_json(data, filename=OUTPUT_FILE):
    """Save city data to JSON."""
    for info in data.values():
        if info.get("population") is not None:
            info["population"] = f"{info['population']:,}"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    top_cities = fetch_top_cities(TOP_N)
    enriched_data = enrich_city(top_cities)
    enriched_data = add_wikipedia_summary_and_image(enriched_data)
    save_to_json(enriched_data)
    print(f"✅ Data saved to {OUTPUT_FILE}")

