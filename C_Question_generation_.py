import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_DATA_FILES = [
    os.path.join(BASE_DIR, "City_Info_API.json"),
    os.path.join(BASE_DIR, "city_info_api.json"),
]
CITY_LIST_FILE = os.path.join(BASE_DIR, "city_list.json")
ALL_QUESTIONS_FILE = os.path.join(BASE_DIR, "all_questions.json")
NUM_CHOICES = 4


def load_city_list():
    """Load the curated list of playable cities."""
    with open(CITY_LIST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_city_data():
    """Load city data from the first available JSON file."""
    for path in CITY_DATA_FILES:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)

    raise FileNotFoundError("No city info JSON file found.")


def generate_questions(city_name, city_data, playable_cities, num_choices=NUM_CHOICES):
    """Generate multiple-choice questions from curated city attributes."""
    if city_name not in city_data:
        raise ValueError(f"{city_name} not found in city data.")

    info = city_data[city_name]
    questions = []

    def get_wrong_choices(correct_city):
        pool = [city for city in playable_cities if city != correct_city]
        return random.sample(pool, num_choices - 1)

    def add_question(question_type, question_text):
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append(
            {
                "question_type": question_type,
                "question": question_text,
                "correct_answer": city_name,
                "options": options,
            }
        )

    languages = info.get("languages", [])
    if languages:
        add_question(
            "languages",
            (
                f"The locals in this city primarily speak "
                f"{', '.join(languages)}. Which city is it?"
            ),
        )

    population = info.get("population")
    if population:
        add_question(
            "population",
            f"This city has a population of {population}. Which city is it?",
        )

    continent = info.get("continent")
    if continent:
        add_question(
            "continent",
            f"This city is located on the continent of {continent}. Which city is it?",
        )

    country = info.get("country")
    if country:
        add_question(
            "country",
            f"This city is in the country {country}. Which city is it?",
        )

    area_km2 = info.get("area_km2")
    if isinstance(area_km2, (int, float)) and area_km2 > 0:
        add_question(
            "area",
            f"This city covers an area of {area_km2:,.2f} km². Which city is it?",
        )

    summary = info.get("summary")
    if summary:
        summary_sentences = summary.split(". ")
        brief_summary = ". ".join(summary_sentences[:2]).strip()
        if brief_summary:
            add_question(
                "summary",
                f"Which city is described as: {brief_summary}?",
            )

    image_url = info.get("image_url")
    if image_url:
        add_question(
            "image",
            f"Identify the city in this image: {image_url}",
        )

    return questions


def generate_all_questions():
    """Generate questions only for curated playable cities."""
    city_data = load_city_data()
    playable_cities = load_city_list()
    all_questions = []

    for city_name in playable_cities:
        if city_name not in city_data:
            continue

        try:
            city_questions = generate_questions(
                city_name,
                city_data,
                playable_cities,
            )
            all_questions.extend(city_questions)
        except (ValueError, KeyError, TypeError):
            continue

    return all_questions


def save_all_questions(all_questions):
    """Save generated questions to JSON."""
    with open(ALL_QUESTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(all_questions, file, indent=2, ensure_ascii=False)


def get_random_question(current_city=None):
    """Return a random question, labeled choices, and correct letter."""
    try:
        with open(ALL_QUESTIONS_FILE, "r", encoding="utf-8") as file:
            all_questions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "⚠️ all_questions.json not found or invalid. "
            "Please generate questions first."
        ) from error

    if not all_questions:
        raise ValueError("⚠️ No questions available in all_questions.json.")

    if current_city:
        city_questions = [
            question
            for question in all_questions
            if question.get("correct_answer", "").lower() == current_city.lower()
        ]
        if not city_questions:
            raise ValueError(f"⚠️ No questions found for city: {current_city}")
        selected = random.choice(city_questions)
    else:
        selected = random.choice(all_questions)

    question_text = selected.get("question", "No question text available.")
    raw_options = selected.get("options", [])
    correct_answer = selected.get("correct_answer")

    letters = ["A", "B", "C", "D"]
    options = [
        f"{letters[index]}. {option}"
        for index, option in enumerate(raw_options[:4])
    ]

    correct_letter = None
    for index, option in enumerate(raw_options[:4]):
        if option.lower() == correct_answer.lower():
            correct_letter = letters[index]
            break

    if correct_letter is None:
        correct_letter = random.choice(letters)

    return question_text, options, correct_letter


if __name__ == "__main__":
    questions = generate_all_questions()
    save_all_questions(questions)
    print(f"✅ Generated {len(questions)} questions and saved to all_questions.json")
