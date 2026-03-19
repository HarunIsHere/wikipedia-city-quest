import json
from tabulate import tabulate  # pip install tabulate

# ----------------------------
# Save & Display Results (Ranked)
# ----------------------------
def save_and_display_results(name, visited, correct_answers, total_time):
    """Save player's results to results.json and display ranked leaderboard."""
    result_self = {
        "Steps taken": len(visited),
        "Correct answers": correct_answers,
        "Total time (s)": total_time,
        "Cities visited": visited,
    }

    # Load existing data
    try:
        with open("results_self.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Update or add player record
    data[name] = result_self

    # Save updated data
    with open("results_self.json", "w") as f:
        json.dump(data, f, indent=4)

    # Sort by: most correct → least time
    sorted_data = sorted(
        data.items(),
        key=lambda x: (
            -x[1]["Correct answers"],   # descending (more correct = better)
            x[1]["Total time (s)"],     # ascending (less time = better)
        )
    )

    # Prepare table
    table = [
        [i + 1, player, stats["Correct answers"], stats["Total time (s)"], stats["Steps taken"]]
        for i, (player, stats) in enumerate(sorted_data)
    ]

    print("\n🏅 Leaderboard (Ranked):")
    print(tabulate(table, headers=["Rank", "Player", "Correct", "Time (s)", "Steps"], tablefmt="fancy_grid"))