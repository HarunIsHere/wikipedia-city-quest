import json
import random
import sys
import time
from time import sleep
import os # os and platform and subprocess needed for clearing console screen
import platform
import subprocess
from colorama import Fore, Style, init
import pygame

# Initialize Audio
home = os.path.expanduser("~")
BASE_DIR = "/Users/harun/Library/Mobile Documents/com~apple~CloudDocs/Hackathlon"
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

sound_files = {
    "game_music": os.path.join(SOUND_DIR, "1-opening-titles.mp3"),
    "correct": os.path.join(SOUND_DIR, "113-midi-fanfare.mp3"),
    "incorrect": os.path.join(SOUND_DIR, "incorrect.mp3"),
}
# Initialize pygame mixer
pygame.mixer.init()

# Initialize colorama
init(autoreset=True)  # automatically resets colors after each print

# Text Styling (text styling only - no background color applied)
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
WHITE = Fore.WHITE
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

def get_cities_list():
    """Load and return the list of cities from city_list.json."""
    with open("city_list.json", "r") as f:
        cities = json.load(f)
    return cities


def get_goal_city(cities, start_city):
    """Return a random goal city different from the start city."""
    available_cities = [c for c in cities if c.lower() != start_city.lower()]
    return random.choice(available_cities)

### Gameplay Styling and Animations ###
def clear_screen():
    """Clears the console safely."""
    try:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            subprocess.run("clear", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("\n" * 75) # fallback fake clear

def type_text(text, delay=0.02):
    """Print text with a typing effect."""
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print()

def transition():
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(0.3)
    clear_screen()

### Game Initialization ###
def setup_game():
    cities = get_cities_list() # Uses loaded city list

    # pygame.mixer.music.load(os.path.join(SOUND_DIR, "game_music.mp3"))
    # correct_sfx = pygame.mixer.Sound(os.path.join(SOUND_DIR, "correct.mp3"))
    # incorrect_sfx = pygame.mixer.Sound(os.path.join(SOUND_DIR, "incorrect.mp3"))

    clear_screen()
    print(f"{RED}{BOLD}████████████████████████████████████████████████████████████████████████████████████{RESET}")
    print(f"{WHITE}{BOLD}     ⚠️ PYTHON INTELLIGENCE AGENCY BULLETIN  - GLOBAL THREAT DETECTED ⚠️           {RESET}")
    print(f"{RED}{BOLD}████████████████████████████████████████████████████████████████████████████████████{RESET}")
    sleep(1)
    clear_screen()

    type_text("\nInitializing connection to the Python Intelligence Agency...")
    transition()
    sleep(1.5)
    type_text("\nConnection established.\n\n")
    sleep(0.6)
    clear_screen()

    type_text("⚠️ Alert! A rogue AI agent known as the “Black Knight” — written in forbidden Python code — has escaped the lab.\nIt’s traveling through global data centers, hiding itself across major cities and rewriting Wikipedia as it goes.\n\nYour mission: track and capture the Black Knight before it gets away - the future of Wikipedia is in your hands!\n\n")
    clear_screen()

    name = input(f" 🌐 Welcome to the Python Intelligence Agency! Please enter your name, Agent: ")
    start_city = input(f" 🌐 Please enter the city you are located: ")

    clear_screen()
    print(f"\n{BOLD}Game Instructions:{RESET}\n")
    type_text(
        "🔹 Track the Black Knight by decoding clues hidden in city data.\n"
        "🔹 Each clue will guide you to the next city. Answer correctly to advance.\n"
        "🔹 Use your knowledge of geography to deduce the correct location.\n"
        "🔹 Answer incorrectly and the code will be scrambled - letting the Black Knight escape further.\n"
        "🔹 Be quick - the Black Knight moves fast. Catch it before it hides in the deepest subnet of the dark web!\n"
    )
    clear_screen()

    goal_city = get_goal_city(cities, start_city)
    path_length = random.randint(4, 4)

    type_text(f"🌐Agent {name}, do you choose to accept the mission?")
    print(input("Press ENTER to accept or press ESC to quit."))
    type_text(f"Note: you may press ESC at any time to quit the mission.")           ### THIS FUNCTION MUST BE ADDED TO MAIN GAME ROUND

    "Storyline text before first question (more storyline in .py and D_ask/check)"

        # f"🌐 November 13th, 8:00 AM, {player_location}"
# You awake to find an urgent message flashing on your computer screen:
# 🧠 Trace log detected: the Black Knight has uploaded a new data fragment!
# (QUESTION) A signal pulse leads to a server cluster beneath a city, encoded in {language}.
# The AI might be using local infrastructure as camouflage.
# In which city is the server located?

    print(f"\n{name}, your journey starts in {start_city} 🌍")
    print(f"Reach to the goal_city 🏁 in {path_length + 1} steps or fewer!\n")

    return name, start_city, goal_city, path_length, cities



# import json
# import random
#
#
# def get_cities_list():
#     """Load and return the list of cities from city_list.json."""
#     with open("city_list.json", "r") as f:
#         cities = json.load(f)
#     return cities
#
#
# def setup_game():
#     """Initialize the game setup using the loaded city list."""
#     cities = get_cities_list()
#
#     print("🎮 Welcome to WiFind – The Wikipedia City Quest!")
#     name = input("Enter your player name: ")
#     start_city = input("In which city are you? ").strip()
#
#     cities = [city for city in cities if city.lower() != start_city.lower()]
#     goal_city = random.choice([c for c in cities if c != start_city])
#     path_length = random.randint(10, 10)
#
#     print(f"\n{name}, your journey starts in {start_city} 🌍")
#     print(f"Your goal is to reach {goal_city} 🏁 in {path_length} steps or fewer!\n")
#
#     return name, start_city, goal_city, path_length, cities

# import json
# import random
# import openai
# import os
#
# # Your API key (keep private)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")#
#
# # ---------------------------
# # 1. Generate 50 cities and save once
# # ---------------------------
# def generate_city_list():
#     prompt = """List 50 of the most important, globally recognized cities
# (at least 3 from each continent: Asia, Europe, Africa, North America,
# South America, and Oceania). Only list the city names, separated by commas."""
#
#     response = openai.chat.completions.create(
#         model="gpt-5-nano",
#         messages=[
#             {"role": "system", "content": "You are a geography assistant."},
#             {"role": "user", "content": prompt},
#         ]
#     )
#
#     city_text = response.choices[0].message.content
#     cities = [city.strip() for city in city_text.split(",") if city.strip()]
#     cities = list(dict.fromkeys(cities))  # remove duplicates
#     return cities
#
#
# # ---------------------------
# # 2. Load existing or create new city list
# # ---------------------------
# def load_or_create_city_list(file_path="city_list.json"):
#     if os.path.exists(file_path):
#         with open(file_path, "r") as f:
#             return json.load(f)
#     else:
#         cities = generate_city_list()
#         with open(file_path, "w") as f:
#             json.dump(cities, f, indent=2)
#         print("✅ City list generated and saved to city_list.json")
#         return cities
#
#
# # ---------------------------
# # 3. Setup game (no arguments)
# # ---------------------------
# def setup_game():
#     cities = load_or_create_city_list()
#
#     print("🎮 Welcome to WiFind – The Wikipedia City Quest!")
#     name = input("Enter your player name: ")
#     start_city = input("In which city are you? ").strip()
#
#     # Clean list
#     cities = [city for city in cities if city.lower() != start_city.lower()]
#
#     goal_city = random.choice([c for c in cities if c != start_city])
#     path_length = random.randint(10, 10)
#
#     print(f"\n{name}, your journey starts in {start_city} 🌍")
#     print(f"Your goal is to reach {goal_city} 🏁 in {path_length} steps or fewer!\n")
#
#     return name, start_city, goal_city, path_length, cities
#
#
# # ---------------------------
# # 4. Entry point
# # ---------------------------
# if __name__ == "__main__":
#     name, start_city, goal_city, path_length, cities = setup_game()



# import json
# import random
# import openai
#
# # Your API key (keep private)
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")#
# with open("City_Info_API.json", "r") as f:
#     City_Info_API = json.load(f)
#
#
# def setup_game():git reset --soft HEAD~1
#     # --- Generate 50 world cities with OpenAI ---
#     prompt = """List 50 of the most important, globally recognized cities
# (at least 3 from each continent: Asia, Europe, Africa, North America,
# South America, and Oceania). Only list the city names, separated by commas."""
#
#     response = openai.chat.completions.create(
#         model="gpt-5-nano",
#         messages=[
#             {"role": "system", "content": "You are a geography assistant."},
#             {"role": "user", "content": prompt},
#         ]
#     )
#
#     city_text = response.choices[0].message.content
#     cities = [city.strip() for city in city_text.split(",") if city.strip()]
#
#     # --- Ask user for starting city ---
#     print("🎮 Welcome to WiFind – The Wikipedia City Quest!")
#     name = input("Enter your player name: ")
#     start_city = input("In which city are you? ").strip()
#
#     # --- Clean up list ---
#     # Remove duplicates and user’s city if present
#     cities = list(dict.fromkeys(cities))
#     cities = [city for city in cities if city.lower() != start_city.lower()]
#
#     # --- Pick target and path length ---
#     goal_city = random.choice([c for c in cities if c != start_city])
#     path_length = random.randint(10, 10)
#
#     print(f"\n{name}, your journey starts in {start_city} 🌍")
#     print(f"Your goal is to reach {goal_city} 🏁 in {path_length} steps or fewer!\n")
#
#     return name, start_city, goal_city, path_length, cities




# import json
# import random
#
# with open("City_Info_API.json", "r") as f:
#     City_Info_API = json.load(f)
#
#
# def setup_game():
#     cities = City_Info_API.keys()
#     print("🎮 Welcome to WiFind – The Wikipedia City Quest!")
#     name = input("Enter your player name: ")
#
#     start_city = random.choice(list(cities))
#     goal_city = random.choice([c for c in cities if c != start_city])
#     path_length = random.randint(10, 10)
#
#     print(f"\n{name}, your journey starts in {start_city} 🌍")
#     print(f"Your goal is to reach {goal_city} 🏁 in {path_length} steps or fewer!\n")
#     return name, start_city, goal_city, path_length, cities