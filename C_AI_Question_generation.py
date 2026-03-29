import os
import random

import openai


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def generate_question(city_name):
    """
    Generate a multiple-choice geography question using OpenAI.

    Returns:
        tuple: (question_text, choices, correct_answer_letter)
    """
    prompt = f"""
    Create a simple geography question where the correct answer is {city_name}.
    The question should involve reasoning (e.g. landmarks, historical facts, or
    nearby regions), not just direct country identification.
    Provide 4 city-name options (A-D), with only one correct.
    Do not reveal or mark which is correct. Format exactly as:
    Question: <text>
    A. <city1>
    B. <city2>
    C. <city3>
    D. <city4>
    """

    response = openai.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {
                "role": "system",
                "content": "You are a quiz question generator.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    text = response.choices[0].message.content.strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    question = ""
    choices = []

    for line in lines:
        if line.startswith("Question:"):
            question = line.replace("Question:", "", 1).strip()
        elif line[:2] in {"A.", "B.", "C.", "D."}:
            choices.append(line)

    correct_answer = None
    for line in choices:
        option_text = line.split(".", 1)[1].strip()
        if option_text.lower() == city_name.lower():
            correct_answer = line.split(".", 1)[0].strip()
            break

    if correct_answer is None:
        correct_answer = random.choice(["A", "B", "C", "D"])

    return question, choices, correct_answer

