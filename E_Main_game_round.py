import A_Set_up
import B_Get_city_info_API
import C_Question_generation_
import B_Wiki_AI_Get_city_summary_API
import C_AI_Question_generation
import D_Ask_and_check_answer
import F_Ranks_AI
import F_Ranks_Self
import random
import time
import json
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
pygame.init()

# ----------------------------
# Load City Data
# ----------------------------
with open("City_Info_API.json", "r") as f:
    City_Info_API = json.load(f)

with open("all_questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Load all pre-fetched summaries once
with open("wiki_city_summaries.json", "r", encoding="utf-8") as f:
    city_summaries = json.load(f)

# ----------------------------
# Initialize Mixer + Load Audio
# ----------------------------
BASE_DIR = "/Users/harun/Library/Mobile Documents/com~apple~CloudDocs/Hackathlon"
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

os.makedirs(SOUND_DIR, exist_ok=True)

sound_files = {
    "game_music": os.path.join(SOUND_DIR, "1-opening-titles.mp3"),
    "correct": os.path.join(SOUND_DIR, "113-midi-fanfare.mp3"),
    "incorrect": os.path.join(SOUND_DIR, "incorrect.mp3"),
}

# # Initialize mixer ===
#
# pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
#
#
# # Assign Sound Paths
# game_music = sound_files["game_music"]
# correct_path = sound_files["correct"]
# incorrect_path = sound_files["incorrect"]
#
# # === Load background music ===
# pygame.mixer.music.load(game_music)
# pygame.mixer.music.set_volume(0.6)
# pygame.mixer.music.play(-1)  # infinite loop
#
#
# # === Load sound effects ===
#
# correct_sfx = pygame.mixer.Sound(correct_path)
# incorrect_sfx = pygame.mixer.Sound(incorrect_path)
# correct_sfx.set_volume(0.9)
# incorrect_sfx.set_volume(0.9)
#
# pygame.mixer.init()
#
# pygame.mixer.music.load(sound_files["game_music"])
# correct_sfx = pygame.mixer.Sound(sound_files["correct"])
# incorrect_sfx = pygame.mixer.Sound(sound_files["incorrect"])
#
# # Start looping intro
# pygame.mixer.music.set_volume(0.6)   # softer background
# pygame.mixer.music.play(-1)          # -1 = infinite loop
#
# # Correct Answer SFX
# correct_sfx = pygame.mixer.Sound(correct_sfx)
# correct_sfx.set_volume(0.9)
# correct_sfx.play()  # plays correct sfx
# time.sleep(2)  # let it finish
#
#
# # Incorrect Answer SFX
# incorrect_sfx = pygame.mixer.Sound(incorrect_sfx)
# incorrect_sfx.set_volume(0.9)
# incorrect_sfx.play()
#
# # Keep playing intro in background
# time.sleep(5)
# pygame.mixer.quit()


# ----------------------------
# Play Round (AI Mode)
# ----------------------------
def play_round_AI(name, start_city, goal_city, path_length, cities):
    current_city = random.choice(A_Set_up.get_cities_list())  # next city after user's city
    visited = [current_city]
    correct_answers = 0
    start_time = time.time()

    for step in range(1, path_length + 1):
        # 🏁 If it’s the last question, switch to the goal city
        if step == path_length or len(visited) == len(cities) - 1:
            current_city = goal_city
            print(f"\n🌍 Final Question! \n")

        question, choices, correct_answer = C_AI_Question_generation.generate_question(current_city)

        B_Wiki_AI_Get_city_summary_API.get_city_summary(current_city)

        if D_Ask_and_check_answer.ask_question(question, choices, correct_answer):
            # correct_sfx.play() # plays correct sfx (in setup file)
            # time.sleep(2)  # let it finish
            print("✅ Correct!\n")
            correct_answers += 1

            # if current_city != goal_city:  # don't move if already at goal
            current_city = random.choice(
                [c for c in A_Set_up.get_cities_list() if c not in visited]
            )
        else:
            # incorrect_sfx.play() # plays incorrect sfx (in setup file)
            # time.sleep(2)  # let it finish
            print("❌ Wrong! Stay where you are.\n")

        visited.append(current_city)

        # if current_city == goal_city:
        #     print(f"🎉 You reached {goal_city} in {step} steps!")
        #     break
    else:
        print(f"🏁 You ran out of steps before reaching {goal_city}.")

    total_time = round(time.time() - start_time, 2)

    # 💾 Save + show leaderboard
    F_Ranks_AI.save_and_display_results(name, visited, correct_answers, total_time)

    return len(visited), total_time

# ----------------------------
# Play Round (Self Generated Questions Mode)
# ----------------------------
def play_round_Self(name, start_city, goal_city, path_length, cities):
    current_city = random.choice(all_questions)["correct_answer"] # next city after users city
    visited = [current_city] # cities visited except the users city
    correct_answers = 0
    start_time = time.time()

    for step in range(1, path_length + 1):

        question, choices, correct_answer = C_Question_generation_.get_random_question(current_city)

        B_Wiki_AI_Get_city_summary_API.get_city_summary(current_city)  # GET CITY SUMMARY

        if D_Ask_and_check_answer.ask_question(question, choices, correct_answer):
            print("✅ Correct!\n")
            correct_answers += 1
            current_city = random.choice(
                [c for c in [c["correct_answer"] for c in all_questions] if c not in visited]
            )
        else:
            print("❌ Wrong! Stay where you are.\n")

        visited.append(current_city)
        if current_city == goal_city:
            print(f"🎉 You reached {goal_city} in {step} steps!")
            break
    else:
        print(f"🏁 You ran out of steps before reaching {goal_city}.")

    total_time = round(time.time() - start_time, 2)

    F_Ranks_Self.save_and_display_results(name, visited, correct_answers, total_time)

    return len(visited), total_time

# ----------------------------
# Main Loop
# ----------------------------
def main():
    while True:
        name, start_city, goal_city, path_length, cities = A_Set_up.setup_game()
        user_choice_AI_or_Self = input("Do you want to play with AI or Self? (A/S): ")

        if user_choice_AI_or_Self.upper() == "A":
            steps, time_used = play_round_AI(name, start_city, goal_city, path_length, cities)
        if user_choice_AI_or_Self.upper() == "S":
            steps, time_used = play_round_Self(name, start_city, goal_city, path_length, cities)

        print(f"\n🏅 Score criteria: more correct answer + less time = better performance.\n")

        again = input("Play again? (y/n): ").lower()
        if again != "y":
            print("Thanks for playing WiFind! 👋")
            break


# ----------------------------
# Run game
# ----------------------------
if __name__ == "__main__":
    main()
