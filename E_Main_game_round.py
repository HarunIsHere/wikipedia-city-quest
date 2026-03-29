import json
import os
import random
import time

import A_Set_up
import B_Wiki_AI_Get_city_summary_API
import C_AI_Question_generation
import C_Question_generation_
import D_Ask_and_check_answer
import F_Ranks_AI
import F_Ranks_Self


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_INFO_FILES = [
    os.path.join(BASE_DIR, "city_info_api.json"),
    os.path.join(BASE_DIR, "City_Info_API.json"),
]
ALL_QUESTIONS_FILE = os.path.join(BASE_DIR, "all_questions.json")


def load_json_file(possible_paths, description):
    """Load JSON data from the first existing file path."""
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)

    raise FileNotFoundError(f"{description} file not found.")


def load_city_info():
    """Load city info JSON."""
    return load_json_file(CITY_INFO_FILES, "City info")


def load_all_questions():
    """Load all generated questions JSON."""
    return load_json_file([ALL_QUESTIONS_FILE], "Questions")


def choose_next_city(available_cities, visited, goal_city, force_goal=False):
    """Choose the next city to target."""
    if force_goal:
        return goal_city

    candidates = [
        city
        for city in available_cities
        if city not in visited and city != goal_city
    ]

    if not candidates:
        return goal_city

    return random.choice(candidates)


def play_round_ai(name, start_city, goal_city, path_length, cities):
    """Play one round using AI-generated questions."""
    current_city = start_city
    visited = [start_city]
    correct_answers = 0
    start_time = time.time()

    for step in range(1, path_length + 1):
        target_city = choose_next_city(
            available_cities=A_Set_up.get_cities_list(),
            visited=visited,
            goal_city=goal_city,
            force_goal=(step == path_length),
        )

        if target_city == goal_city:
            print("\n🌍 Final Question!\n")

        question, choices, correct_answer = (
            C_AI_Question_generation.generate_question(target_city)
        )

        B_Wiki_AI_Get_city_summary_API.get_city_summary(target_city)

        if D_Ask_and_check_answer.ask_question(
            question,
            choices,
            correct_answer,
        ):
            print("✅ Correct!\n")
            correct_answers += 1
            current_city = target_city
            visited.append(current_city)

            if current_city == goal_city:
                print(f"🎉 You reached {goal_city} in {step} steps!")
                break
        else:
            print(f"❌ Wrong! You remain in {current_city}.\n")
    else:
        print(f"🏁 You ran out of steps before reaching {goal_city}.")

    total_time = round(time.time() - start_time, 2)
    F_Ranks_AI.save_and_display_results(
        name,
        visited,
        correct_answers,
        total_time,
    )

    return len(visited), total_time


def play_round_self(name, start_city, goal_city, path_length, cities):
    """Play one round using self-generated questions."""
    all_questions = load_all_questions()
    all_cities = list({item["correct_answer"] for item in all_questions})

    current_city = start_city
    visited = [start_city]
    correct_answers = 0
    start_time = time.time()

    for step in range(1, path_length + 1):
        target_city = choose_next_city(
            available_cities=all_cities,
            visited=visited,
            goal_city=goal_city,
            force_goal=(step == path_length),
        )

        if target_city == goal_city:
            print("\n🌍 Final Question!\n")

        question, choices, correct_answer = (
            C_Question_generation_.get_random_question(target_city)
        )

        B_Wiki_AI_Get_city_summary_API.get_city_summary(target_city)

        if D_Ask_and_check_answer.ask_question(
            question,
            choices,
            correct_answer,
        ):
            print("✅ Correct!\n")
            correct_answers += 1
            current_city = target_city
            visited.append(current_city)

            if current_city == goal_city:
                print(f"🎉 You reached {goal_city} in {step} steps!")
                break
        else:
            print(f"❌ Wrong! You remain in {current_city}.\n")
    else:
        print(f"🏁 You ran out of steps before reaching {goal_city}.")

    total_time = round(time.time() - start_time, 2)
    F_Ranks_Self.save_and_display_results(
        name,
        visited,
        correct_answers,
        total_time,
    )

    return len(visited), total_time


def main():
    """Run the game loop."""
    load_city_info()

    while True:
        name, start_city, goal_city, path_length, cities = A_Set_up.setup_game()

        user_choice_ai_or_self = input(
            "Do you want to play with AI or Self? (A/S): "
        ).strip().upper()

        while user_choice_ai_or_self not in {"A", "S"}:
            user_choice_ai_or_self = input(
                "Please enter A for AI or S for Self: "
            ).strip().upper()

        if user_choice_ai_or_self == "A":
            play_round_ai(name, start_city, goal_city, path_length, cities)
        else:
            play_round_self(name, start_city, goal_city, path_length, cities)

        print(
            "\n🏅 Score criteria: more correct answers + less time = "
            "better performance.\n"
        )

        again = input("Play again? (y/n): ").strip().lower()
        while again not in {"y", "n"}:
            again = input("Please enter y or n: ").strip().lower()

        if again != "y":
            print("Thanks for playing WiFind! 👋")
            break


if __name__ == "__main__":
    main()
