import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_DATA_FILE = os.path.join(BASE_DIR, "city_info_api.json")
ALL_QUESTIONS_FILE = os.path.join(BASE_DIR, "all_questions.json")
NUM_CHOICES = 4


def load_city_data():
    """Load city data from JSON."""
    with open(CITY_DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_questions(city_name, city_data, num_choices=NUM_CHOICES):
    """Generate multiple-choice questions from city attributes."""
    city_names = list(city_data.keys())

    if city_name not in city_names:
        raise ValueError(f"{city_name} not found in city data.")

    info = city_data[city_name]
    questions = []

    def get_wrong_choices(correct):
        available = [city for city in city_names if city != correct]
        return random.sample(available, num_choices - 1)

    def make_question(question_type, question_text):
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

    if info.get("languages"):
        langs = ", ".join(info["languages"])
        make_question(
            "languages",
            f"The locals in this city primarily speak {langs}. Which city is it?",
        )

    if info.get("population"):
        make_question(
            "population",
            (
                f"This city has a population of {info['population']}. "
                "Which city is it?"
            ),
        )

    if info.get("continent"):
        make_question(
            "continent",
            (
                f"This city is located on the continent of {info['continent']}. "
                "Which city is it?"
            ),
        )

    if info.get("country"):
        make_question(
            "country",
            f"This city is in the country {info['country']}. Which city is it?",
        )

    if info.get("area_km2"):
        area_val = info["area_km2"]
        if isinstance(area_val, list):
            area_val = area_val[0]

        make_question(
            "area",
            f"This city covers an area of {area_val:,.2f} km². Which city is it?",
        )

    if info.get("highestPoint_m"):
        height_val = info["highestPoint_m"]
        if isinstance(height_val, list):
            height_val = height_val[0]

        make_question(
            "highest_point",
            (
                f"The highest point in this city reaches {height_val} meters. "
                "Which city is it?"
            ),
        )

    if info.get("summary"):
        summary_text = info["summary"].split(". ")
        brief_summary = ". ".join(summary_text[:2])
        make_question(
            "summary",
            f"Which city is described as: {brief_summary}?",
        )

    if info.get("image_url"):
        make_question(
            "image",
            f"Identify the city in this image: {info['image_url']}",
        )

    return questions


def generate_all_questions():
    """Generate questions for all cities."""
    city_data = load_city_data()
    all_questions = []

    for city_name in city_data:
        try:
            all_questions.extend(generate_questions(city_name, city_data))
        except (ValueError, KeyError, TypeError):
            continue

    return all_questions


def save_all_questions(all_questions):
    """Save generated questions to JSON."""
    with open(ALL_QUESTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(all_questions, file, indent=2, ensure_ascii=False)


def get_random_question(current_city=None):
    """Return a random question, choices, and correct letter."""
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

    correct = None
    for index, option in enumerate(raw_options[:4]):
        if option.lower() == correct_answer.lower():
            correct = letters[index]
            break

    if correct is None:
        correct = random.choice(letters)

    return question_text, options, correct


if __name__ == "__main__":
    questions = generate_all_questions()
    save_all_questions(questions)
