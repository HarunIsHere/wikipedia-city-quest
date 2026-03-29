import json
import os
import platform
import random
import subprocess
import time
from time import sleep

from colorama import Fore, Style, init

try:
    import pygame
except ImportError:
    pygame = None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITY_LIST_FILE = os.path.join(BASE_DIR, "city_list.json")
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

sound_files = {
    "game_music": os.path.join(SOUND_DIR, "1-opening-titles.mp3"),
    "correct": os.path.join(SOUND_DIR, "113-midi-fanfare.mp3"),
    "incorrect": os.path.join(SOUND_DIR, "incorrect.mp3"),
}


def init_audio():
    """Initialize pygame mixer if pygame is available."""
    if pygame is None:
        return

    try:
        pygame.mixer.init()
    except pygame.error:
        pass


init_audio()
init(autoreset=True)

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
    with open(CITY_LIST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_goal_city(cities, start_city):
    """Return a random goal city different from the start city."""
    available_cities = [
        city for city in cities if city.lower() != start_city.lower()
    ]
    return random.choice(available_cities)


def clear_screen():
    """Clear the console safely."""
    try:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            subprocess.run(
                ["clear"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except OSError:
        print("\n" * 75)


def type_text(text, delay=0.02):
    """Print text with a typing effect."""
    for char in text:
        print(char, end="", flush=True)
        sleep(delay)
    print()


def transition():
    """Show a short transition animation and clear the screen."""
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.3)
    clear_screen()


def setup_game():
    """Set up the game and return the starting values."""
    cities = get_cities_list()

    clear_screen()
    print(
        f"{RED}{BOLD}"
        "████████████████████████████████████████████████████████████████████████████████████"
        f"{RESET}"
    )
    print(
        f"{WHITE}{BOLD}"
        "     ⚠️ PYTHON INTELLIGENCE AGENCY BULLETIN  - GLOBAL THREAT DETECTED ⚠️           "
        f"{RESET}"
    )
    print(
        f"{RED}{BOLD}"
        "████████████████████████████████████████████████████████████████████████████████████"
        f"{RESET}"
    )
    sleep(1)
    clear_screen()

    type_text("\nInitializing connection to the Python Intelligence Agency...")
    transition()
    sleep(1.5)
    type_text("\nConnection established.\n\n")
    sleep(0.6)
    clear_screen()

    type_text(
        "⚠️ Alert! A rogue AI agent known as the \"Black Knight\" - written "
        "in forbidden Python code - has escaped the lab.\n"
        "It is traveling through global data centers, hiding itself across "
        "major cities and rewriting Wikipedia as it goes.\n\n"
        "Your mission: track and capture the Black Knight before it gets "
        "away - the future of Wikipedia is in your hands!\n\n"
    )
    clear_screen()

    name = input(
        " 🌐 Welcome to the Python Intelligence Agency! "
        "Please enter your name, Agent: "
    ).strip()

    start_city = input(
        " 🌐 Please enter the city you are located in: "
    ).strip()

    while not start_city:
        start_city = input(
            " 🌐 Please enter the city you are located in: "
        ).strip()

    clear_screen()
    print(f"\n{BOLD}Game Instructions:{RESET}\n")
    type_text(
        "🔹 Track the Black Knight by decoding clues hidden in city data.\n"
        "🔹 Each clue will guide you to the next city. Answer correctly to advance.\n"
        "🔹 Use your knowledge of geography to deduce the correct location.\n"
        "🔹 Answer incorrectly and the code will be scrambled - letting the "
        "Black Knight escape further.\n"
        "🔹 Be quick - the Black Knight moves fast. Catch it before it hides "
        "in the deepest subnet of the dark web!\n"
    )
    clear_screen()

    goal_city = get_goal_city(cities, start_city)
    path_length = 4

    type_text(f"🌐 Agent {name}, do you choose to accept the mission?")
    accept = input("Press ENTER to accept or type Q to quit: ").strip().upper()
    if accept == "Q":
        raise SystemExit("Mission aborted.")

    type_text("Note: type Q whenever prompted to quit the mission.")

    print(f"\n{name}, your journey starts in {start_city} 🌍")
    print(f"Reach {goal_city} 🏁 in {path_length} steps or fewer!\n")

    return name, start_city, goal_city, path_length, cities
