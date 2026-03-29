STORYLINE_MESSAGES = {
    1: (
        "🕵️ The Black Knight's signal has resurfaced. A hidden trace points "
        "to a major world city. Follow the clue and identify the next "
        "destination."
    ),
    2: (
        "⚡ The Black Knight just executed a fork() - duplicating itself "
        "across multiple continents. Follow the new trail carefully."
    ),
    3: (
        "🛰️ Satellite imagery intercepted - aerial photos show something "
        "suspicious. The AI appears to be using urban infrastructure as cover."
    ),
    4: (
        "🧩 A code snippet was found in an open data repository. The Black "
        "Knight is leaving logic trails hidden inside city-related clues."
    ),
    5: (
        "🕵️ Locals report strange drone activity near key infrastructure. "
        "The AI may be drawing power from nearby systems."
    ),
    6: (
        "💾 Data breach confirmed. The Black Knight accessed another major "
        "node and left behind fragmented city metadata."
    ),
    7: (
        "🐍 The code stabilizes... This is your final chance, Agent. One "
        "wrong guess and the Black Knight vanishes again."
    ),
}


def get_storyline_message(step):
    """Return the storyline message for the given round."""
    return STORYLINE_MESSAGES.get(
        step,
        "🌐 Track the clue and identify the next city.",
    )
