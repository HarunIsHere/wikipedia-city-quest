import json
import random

CITY_DATA_FILE = "city_info_api.json"
ALL_QUESTIONS_FILE = "all_questions.json"
NUM_CHOICES = 4

# Load city data
with open(CITY_DATA_FILE, "r", encoding="utf-8") as f:
    city_data = json.load(f)

all_questions = []

def generate_questions(city_name, city_data, num_choices=NUM_CHOICES):
    """
    Generate multiple-choice questions from various city attributes.
    Returns a list of question dicts.
    """
    city_names = list(city_data.keys())
    if city_name not in city_names:
        raise ValueError(f"{city_name} not found in city data.")

    info = city_data[city_name]

    questions = []

    # Helper to pick wrong options
    def get_wrong_choices(correct):
        return random.sample([c for c in city_names if c != correct], num_choices - 1)

    # languages
    if info.get("languages"):
        langs = ", ".join(info["languages"])
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append({
            "question_type": "languages",
            "question": f"The locals in this city primarily speak {langs}. Which city is it?",
            "correct_answer": city_name,
            "options": options
        })

    # population
    if info.get("population"):
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append({
            "question_type": "population",
            "question": f"This city has a population of {info['population']}. Which city is it?",
            "correct_answer": city_name,
            "options": options
        })

    # continent
    if info.get("continent"):
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append({
            "question_type": "continent",
            "question": f"This city is located on the continent of {info['continent']}. Which city is it?",
            "correct_answer": city_name,
            "options": options
        })

    # country
    if info.get("country"):
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append({
            "question_type": "country",
            "question": f"This city is in the country {info['country']}. Which city is it?",
            "correct_answer": city_name,
            "options": options
        })

    # area
    if info.get("area_km2"):
        area_val = info["area_km2"][0]
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append({
            "question_type": "area",
            "question": f"This city covers an area of {area_val:,.2f} km². Which city is it?",
            "correct_answer": city_name,
            "options": options
        })

    # highest point
    if info.get("highestPoint_m"):
        height_val = info["highestPoint_m"][0]
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append({
            "question_type": "highest_point",
            "question": f"The highest point in this city reaches {height_val} meters. Which city is it?",
            "correct_answer": city_name,
            "options": options
        })

    # summary
    if info.get("summary"):
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        summary_text = info["summary"].split(". ")
        brief_summary = ". ".join(summary_text[:2])  # first 2 sentences
        questions.append({
            "question_type": "summary",
            "question": f"Which city is described as: {brief_summary}?",
            "correct_answer": city_name,
            "options": options
        })

    # image_url (optional)
    if info.get("image_url"):
        options = get_wrong_choices(city_name) + [city_name]
        random.shuffle(options)
        questions.append({
            "question_type": "image",
            "question": f"Identify the city in this image: {info['image_url']}",
            "correct_answer": city_name,
            "options": options
        })

    return questions


# Generate questions for all cities
for city_name in city_data.keys():
    try:
        city_questions = generate_questions(city_name, city_data)
        all_questions.extend(city_questions)
    except Exception:
        pass
        # print(f"⚠️ Could not generate questions for {city_name}: {e}")

# Save to JSON
with open(ALL_QUESTIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(all_questions, f, indent=2, ensure_ascii=False)

# print(f"✅ Generated {len(all_questions)} questions from city attributes.")


def get_random_question(current_city=None):
    """
    Fetch a random question from all_questions.json.
    If current_city is provided, select a question whose correct_answer matches that city.
    Returns (question, choices_with_letters, correct_letter)
    but keeps original variable names: question_text, options, correct.
    """
    try:
        with open(ALL_QUESTIONS_FILE, "r", encoding="utf-8") as f:
            all_questions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise RuntimeError("⚠️ all_questions.json not found or invalid. Please generate questions first.")

    if not all_questions:
        raise ValueError("⚠️ No questions available in all_questions.json.")

    # Filter by city if provided
    if current_city:
        city_questions = [q for q in all_questions if q.get("correct_answer", "").lower() == current_city.lower()]
        if not city_questions:
            raise ValueError(f"⚠️ No questions found for city: {current_city}")
        selected = random.choice(city_questions)
    else:
        selected = random.choice(all_questions)

    question_text = selected.get("question", "No question text available.")
    raw_options = selected.get("options", [])
    correct_answer = selected.get("correct_answer", None)

    # Attach letters A–D
    letters = ["A", "B", "C", "D"]
    options = [f"{letters[i]}. {opt}" for i, opt in enumerate(raw_options[:4])]

    # Match correct answer to its letter
    correct = None
    for i, opt in enumerate(raw_options[:4]):
        if opt.lower() == correct_answer.lower():
            correct = letters[i]
            break

    if not correct:
        correct = random.choice(letters)

    return question_text, options, correct


# def get_random_question(current_city=None):
#     """
#     Fetch a random question from all_questions.json.
#     If current_city is provided, select a question whose correct_answer matches that city.
#     Returns (question, choices, correct_answer).
#     """
#     try:
#         with open(ALL_QUESTIONS_FILE, "r", encoding="utf-8") as f:
#             all_questions = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         raise RuntimeError("⚠️ all_questions.json not found or invalid. Please generate questions first.")
#
#     if not all_questions:
#         raise ValueError("⚠️ No questions available in all_questions.json.")
#
#     # Filter by city if provided
#     if current_city:
#         city_questions = [q for q in all_questions if q.get("correct_answer", "").lower() == current_city.lower()]
#         if not city_questions:
#             raise ValueError(f"⚠️ No questions found for city: {current_city}")
#         selected = random.choice(city_questions)
#     else:
#         selected = random.choice(all_questions)
#
#     question_text = selected.get("question", "No question text available.")
#     options = selected.get("options", [])
#     correct = selected.get("correct_answer", None)
#
#     return question_text, options, correct