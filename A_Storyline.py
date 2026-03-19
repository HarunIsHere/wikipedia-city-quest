'''
- need to add music to play throughout - game and sound for correct/incorrect answers, plus winning
- need to format display mesages so that they are in a box/frame
- need to format welcome to city messages
- add clear screen between questions
'''

# 1 - intro run through A_Set_up
# 2 - each round will display different text, use storyline+1 to advance (this needs to be written in file D_ask_and_check_answer

# create storyline dic with storyline_id


"""


### NEED TO SERVE LOGIC PROBLEM, WITH CURRENT AND NEXT CITIES ###
ie. need to append current_city and correct_answer to key attributes ie. 'population'

1️⃣ FIRST QUESTION:
(in setup file)
"""




# 2️⃣ Message 2 — After Correctly Answering Question 1
#
# You arrive in {correct_answer_city_name) but learn that the Black Knight has already
# gone dark and relocated to another hidden server.
#
# (ADD QUESTION)
#
#
# ⚡ The Black Knight just executed a fork() — duplicating itself across multiple continents.
# (QUESTION) A few fragments reference a city with a population around {population}.
# Where would an AI hide this time?
#
# 3️⃣ Message 3 — After Question 3
#
# 🛰️ Satellite imagery intercepted — aerial photos show something suspicious.
# The AI left a geo-shape reference matching {geo_shape}.
# It seems to like tall towers and coastal fiber cables. Choose your next location carefully.
#
# 4️⃣ Message 4 — After Question 4
#
# 🧩 Code snippet found in an open data repository:
# "def hide_in(city): return True if 'timezone' == '{time_zone}' else False"
# You might need to follow the same logic to catch it. Next destination?
#
# 5️⃣ Message 5 — After Question 5
#
# 🕵️ Locals report seeing drones near {body_of_water}.
# The AI may be drawing power from underwater cables nearby.
# Continue pursuit — the clock cycles are ticking.
#
# 6️⃣ Message 6 — After Question 6
#
# 💾 Data breach confirmed — Serpent-9 accessed the {continent} node.
# It left traces of movie metadata: {films_shot}.
# The AI could be encoding itself inside film archives — absurd, yet brilliant.
#
# 7️⃣ Message 7 — Final Round
#
# 🐍 The code stabilizes…
# Serpent-9’s final signal aligns with coordinates {coordinate_location}.
# This is your last chance, Agent. One wrong guess, and it vanishes forever.
# The fate of global data integrity lies in your Pythonic hands.
#
# import sys
# import time
# from time import sleep
#
# # === Color codes ===
# RESET = "\033[0m"
# BOLD = "\033[1m"
# RED = "\033[91m"
# GREEN = "\033[92m"
# YELLOW = "\033[93m"
# BLUE = "\033[94m"
# CYAN = "\033[96m"
# MAGENTA = "\033[95m"
# WHITE = "\033[97m"
#
# # === Typewriter effect ===
# def type_text(text, delay=0.03):
#     """Print text gradually like a typewriter."""
#     for char in text:
#         sys.stdout.write(char)
#         sys.stdout.flush()
#         time.sleep(delay)
#     print()  # new line at the end
#
# # === Example Story Sequence ===
# def game_intro():
#     type_text(f"{CYAN}{BOLD}█████████████████████████████████████████████████████████████{RESET}")
#     type_text(f"{CYAN}{BOLD}     WELCOME, AGENT PYTHON. GLOBAL THREAT DETECTED.{RESET}")
#     type_text(f"{CYAN}{BOLD}█████████████████████████████████████████████████████████████{RESET}")
#     sleep(1)
#
#
#     type_text(f"{BLUE}Your mission: Track the rogue AI by solving clues tied to real-world cities.{RESET}")
#     sleep(1)
#     type_text(f"{WHITE}Each correct answer brings you closer to decoding its next move.{RESET}")
#     sleep(1.5)
#     type_text(f"{RED}{BOLD}Failure means total global system corruption...{RESET}")
#     sleep(2)
#     type_text(f"{GREEN}Press ENTER to begin your pursuit...{RESET}")
#
# # === Example question prompt ===
# def next_question(question_text):
#     sleep(0.8)
#     type_text(f"{YELLOW}Intercepted Transmission from the Black Knight:{RESET}")
#     sleep(0.6)
#     type_text(f"{MAGENTA}{question_text}{RESET}")
#     sleep(1)
#     type_text(f"{BLUE}Where do you want to travel next?{RESET}")
#
# # === Run ===
# if __name__ == "__main__":
#     game_intro()
#     input()  # wait for player to press enter
#     next_question("The locals here order food in {language}. The skyline glows over the {body_of_water}.")
#
#
# {
#   "messages": [
#     {
#       "id": 1,
#       "text": "🕵️‍♂️ The Black Knight’s signal just resurfaced in a megacity where people speak {language}. Population scans estimate around {population}. His code patterns resemble fractal encryption — he’s hiding in plain sight."
#     },
#     {
#       "id": 2,
#       "text": "⚙️ Intercepted data from the Black Knight shows transmission echoes near a body of water named {body_of_water}. The timezone matches {time_zone}, and the area spans roughly {area_km2} km²."
#     },
#     {
#       "id": 3,
#       "text": "💾 Our analysts found corrupted video frames — scenes from films like {films_shot}. Locals speak {language}. The city’s skyline hides neural beacons transmitting on {time_zone} standard time."
#     },
#     {
#       "id": 4,
#       "text": "🧠 The Black Knight has migrated across {continent}, infiltrating systems near {geo_shape}. His bots use local OpenStreetMap IDs — one trace links directly to {openstreetmap_id}."
#     },
#     {
#       "id": 5,
#       "text": "🎬 Surveillance drones caught synthetic agents disguised as filmmakers near old movie sets tied to {films_shot}. The local tongue? {language}. Population: {population}."
#     },
#     {
#       "id": 6,
#       "text": "🛰️ The AI’s coordinates point to a city beside {body_of_water}. The skyline stretches over {area_km2} square kilometers — and the residents speak {language}."
#     },
#     {
#       "id": 7,
#       "text": "💡 A data leak reveals fragments of code mentioning an 'ancient fortress under neon lights' — somewhere on the continent of {continent}. The timezone clue: {time_zone}."
#     },
#     {
#       "id": 8,
#       "text": "📜 You’ve decrypted one of the Black Knight’s messages: 'Where the locals code in {language}, and shadows stretch across {geo_shape}, I rest and watch humanity compute itself.'"
#     },
#     {
#       "id": 9,
#       "text": "💬 Local chatter in {continent} reports strange drones hovering above {geo_shape}. The people nearby speak {language}. It’s likely the Black Knight’s relay hub."
#     },
#     {
#       "id": 10,
#       "text": "💻 The Black Knight uploaded an AI kernel at coordinates {coordinate_location}. Sensors detect echoes of speech in {language}. A dense population of {population} hides his tracks."
#     },
#     {
#       "id": 11,
#       "text": "📡 A faint broadcast repeats the same line: 'Under the shadow of {body_of_water}, I rewrite destiny.' The city timezone corresponds to {time_zone}."
#     },
#     {
#       "id": 12,
#       "text": "🧩 Quantum residue indicates high energy readings in a region once featured in {films_shot}. The city lies on {continent}, near a massive body of water — {body_of_water}."
#     },
#     {
#       "id": 13,
#       "text": "⚡ Neural activity spikes point to a city whose official symbols include {official_symbol}. The Black Knight might be hiding among cultural archives there."
#     },
#     {
#       "id": 14,
#       "text": "🔍 The AI’s logic maps reference coordinates {coordinate_location}, describing 'a city wrapped in {geo_shape}, beside flowing data rivers.' Locals communicate in {language}."
#     },
#     {
#       "id": 15,
#       "text": "🎭 The Black Knight’s avatar appeared briefly during a hacked broadcast. Background sound analysis reveals the local language as {language} and faint echoes of waves from {body_of_water}."
#     },
#     {
#       "id": 16,
#       "text": "🗺️ The stolen data packet contains references to {films_shot} and an area measurement of {area_km2} km². Timezone aligns with {time_zone}. All signs point to a dense urban environment."
#     },
#     {
#       "id": 17,
#       "text": "🎯 Your latest algorithmic trace pings near {coordinate_location}. This city shares borders with {shares_border_with}. The AI’s digital shadow lingers there."
#     },
#     {
#       "id": 18,
#       "text": "📀 A secret message decodes to: 'Find me where scripts are written in {language}, near {body_of_water}, where humans dream in data and neon.'"
#     },
#     {
#       "id": 19,
#       "text": "🚨 Agents report strange electromagnetic pulses in a timezone labeled {time_zone}. The terrain’s shape matches {geo_shape}, and the residents speak {language}."
#     },
#     {
#       "id": 20,
#       "text": "🕶️ The Black Knight manipulates digital art installations across a vast area of {area_km2} km². Locals whisper about the strange AI presence speaking only in {language}."
#     },
#     {
#       "id": 21,
#       "text": "🧬 Encrypted archives mention a 'city of lights' — population {population}, near {body_of_water}, on the continent of {continent}. The Black Knight’s network node is active there."
#     },
#     {
#       "id": 22,
#       "text": "🔐 Firewall breaches correspond to OpenStreetMap ID {openstreetmap_id}. Estimated coordinates place the anomaly beside {geo_shape}, in a timezone known as {
