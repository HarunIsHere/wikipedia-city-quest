import openai
import os
import random

# Please do not share your key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_question(city_name):
    """
    Generates a multiple-choice question using ChatGPT.
    Returns: (question (text), choices (list), correct_answer)
    """

    prompt = f"""
    Create a simple geography question where the correct answer is {city_name}.
    The question should involve reasoning (e.g. landmarks, historical facts, or nearby regions),
    not just direct country identification.
    Provide 4 city-name options (A–D), with only one correct.
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
            {"role": "system", "content": "You are a quiz question generator."},
            {"role": "user", "content": prompt},
        ]
    )

    text = response.choices[0].message.content.strip()
    lines = text.splitlines()
    question = lines[0].replace("Question:", "").strip()
    choices = [line.strip() for line in lines[1:] if line.strip()]

    # Determine correct answer
    correct_answer = None
    for line in choices:
        if city_name.lower() in line.lower():
            correct_answer = line.split(".")[0].strip()
            break

    # Fallback if not detected
    if not correct_answer:
        correct_answer = random.choice(["A", "B", "C", "D"])

    return question, choices, correct_answer



# import openai
# import os
# import random
#
# # Please do not share your key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")#
# def generate_question(city_name):
#     """
#     Generates a multiple-choice question using ChatGPT.
#     Returns: (question (text), choices (list), correct_answer)
#     Retries if the correct city name is missing from the model’s output.
#     """
#     prompt = f"""
#     Create a simple geography question where the correct answer is {city_name}.
#     The question should involve reasoning (e.g. landmarks, historical facts, or nearby regions),
#     not just direct country identification.
#     Provide 5 city-name options (A–D), with only one correct.
#     Do not reveal or mark which is correct. Format exactly as:
#     Question: <text>
#     A. <city1>
#     B. <city2>
#     C. <city3>
#     D. <city4>
#     """
#
#     max_attempts = 3  # retry limit
#     for attempt in range(max_attempts):
#         response = openai.chat.completions.create(
#             model="gpt-5-nano",
#             messages=[
#                 {"role": "system", "content": "You are a quiz question generator."},
#                 {"role": "user", "content": prompt},
#             ]
#         )
#
#         text = response.choices[0].message.content.strip()
#         lines = text.splitlines()
#         question = lines[0].replace("Question:", "").strip()
#         choices = [line.strip() for line in lines[1:] if line.strip()]
#
#         correct_answer = None
#         for line in choices:
#             if city_name.lower() in line.lower():
#                 correct_answer = line.split(".")[0].strip()
#                 break
#
#         if correct_answer:
#             # ✅ Found a valid question
#             return question, choices, correct_answer
#         else:
#             print(f"⚠️ Attempt {attempt + 1}: city not found in options, retrying...")
#
#     # ❌ After 3 failed attempts
#     print("❌ Failed to generate valid question after 3 attempts.")
#     return question, choices, random.choice(["A", "B", "C", "D"])


# --- Test ---
# print(generate_question("Lahore Division"))

