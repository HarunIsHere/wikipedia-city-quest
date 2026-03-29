import textwrap


def ask_question(question, choices, correct_answer):
    """Display a question, collect a valid answer, and return True or False."""
    print()
    print(textwrap.fill(question, width=80))
    print()

    for choice in choices:
        print(choice)

    print()

    while True:
        user_choice = input("Please choose A, B, C or D: ").strip().upper()

        if user_choice == "Q":
            raise SystemExit("Mission aborted.")

        if user_choice in {"A", "B", "C", "D"}:
            break

        print("Please enter a valid answer: A, B, C or D.")

    return user_choice == correct_answer.strip().upper()
