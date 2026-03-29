import json

from tabulate import tabulate


def save_and_display_results(name, visited, correct_answers, total_time):
    """Save player's results to results.json and display ranked leaderboard."""
    result = {
        "Steps taken": len(visited),
        "Correct answers": correct_answers,
        "Total time (s)": total_time,
        "Cities visited": visited,
    }

    try:
        with open("results.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[name] = result

    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    sorted_data = sorted(
        data.items(),
        key=lambda item: (
            -item[1]["Correct answers"],
            item[1]["Total time (s)"],
        ),
    )

    table = [
        [
            index + 1,
            player,
            stats["Correct answers"],
            stats["Total time (s)"],
            stats["Steps taken"],
        ]
        for index, (player, stats) in enumerate(sorted_data)
    ]

    print("\n🏅 Leaderboard (Ranked):")
    print(
        tabulate(
            table,
            headers=["Rank", "Player", "Correct", "Time (s)", "Steps"],
            tablefmt="fancy_grid",
        )
    )
