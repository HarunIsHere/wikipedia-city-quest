# def normalize_string(text):
#     """Cleans up a string for comparison by lowercase, stripping spaces and removing other non alphanumeric char"""
#     text = text.strip().lower()
#     for char in " ,.!@#$%^&*()_+][{}:~`":
#         text = text.replace(char, "")
#     return text
# def normalize_correct_answer(correct_answer):
#     correct_answer = correct_answer.strip().lower()
#     for char in " ,.!@#$%^&*():_+":
#         correct_answer = correct_answer.replace(char, "")
#     return correct_answer
#
# def check_answer(user_answer, correct_answer):
#     normalized_user = normalize_string(user_answer)
#     correct_answer = normalize_correct_answer(correct_answer)
#     if normalized_user == correct_answer:
#         print("Correct!")
#     else :
#         print("Incorrect!")
#     return normalized_user == correct_answer

import textwrap


def ask_question(question, choices, correct_answer):
    # PRINT MESSAGE (each round has different text, use messages+1 to advance each step)
    print()
    # new_question = textwrap.fill(question, width=80)
    # print(new_question)
    print(question)
    print()
    # new_choices = textwrap.fill(choices, width=80)
    # print(new_choices)
    print(choices)
    print()
    user_choice = input("Please choose A, B, C or D: ")
    user_choice_corrected = user_choice.upper()
    if correct_answer in ["A", "B", "C", "D"]:
        if correct_answer == user_choice_corrected:
            return True
        else:
            return False
    # else : print("Please enter a valid answer(A, B, C or D).")





# Alis update of ask_question
# def ask_question(question, choices, correct_answer):
#     print(question)
#     print()
#     print(correct_answer)
#     correct = correct_answer.strip().upper()
#     user_choice = input("Enter your choice:").strip().upper()
#     while user_choice not in ["A", "B", "C", "D"]:
#         user_choice = input("Enter your choice:").strip().upper()
#         if user_choice == correct_answer:
#             return True


# Testing
# print("What is the capital of France?")
# print("A: Paris, B: London, C: New York, D: Berlin")
# test = ask_question("", "A")  # First parameter is unused in this case
# if test:
#     print("Correct!")
# else:
#     print("Incorrect!")
