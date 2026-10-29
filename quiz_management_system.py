"""
Quiz Management System
A console based quiz program written in Python.

Admin   : add, view and delete questions, load sample questions,
          view and clear student results
Student : choose a category and number of questions, take the quiz,
          see the score with a review of wrong answers

How the randomness works
  - Every quiz picks a fresh random set of questions from the bank.
  - The questions come in a random order.
  - The four options of each question are also shuffled every time.

Data is stored in two JSON files:
  questions.json  -> the question bank
  results.json    -> the saved student results
"""

import json
import os
import random
from datetime import datetime

QUESTIONS_FILE = "questions.json"
RESULTS_FILE = "results.json"

# Admin login details (change them if you want)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ---------------------------------------------------------------
# Sample question bank
# Each item is: (question, correct answer, [three wrong answers])
# ---------------------------------------------------------------
SAMPLE_DATA = {
    "Python Basics": [
        ("Which symbol is used for single line comments in Python?",
         "#", ["//", "/*", "--"]),
        ("Which function is used to take input from the user?",
         "input()", ["get()", "scan()", "read()"]),
        ("What is the file extension of a Python program?",
         ".py", [".python", ".pt", ".pyt"]),
        ("Which function is used to display output on the screen?",
         "print()", ["show()", "display()", "echo()"]),
        ("What is the output of 3 ** 2 ?",
         "9", ["6", "5", "32"]),
        ("Python is which type of language?",
         "Interpreted", ["Compiled", "Assembly", "Machine language"]),
        ("Which operator is used for floor division?",
         "//", ["/", "%", "**"]),
        ("What is the output of 10 % 3 ?",
         "1", ["3", "0", "3.33"]),
        ("Who created the Python language?",
         "Guido van Rossum", ["Dennis Ritchie", "James Gosling", "Bjarne Stroustrup"]),
        ("Which of these is a valid variable name in Python?",
         "my_var", ["2value", "my-var", "my var"]),
    ],
    "Data Types": [
        ("What is the data type of 5.0 in Python?",
         "float", ["int", "str", "double"]),
        ("Which of these data types is immutable?",
         "tuple", ["list", "dict", "set"]),
        ("Which data type stores values as key-value pairs?",
         "dict", ["list", "tuple", "set"]),
        ("What is the data type of True in Python?",
         "bool", ["str", "float", "char"]),
        ("Which function converts the string '10' into an integer?",
         "int()", ["str()", "float()", "num()"]),
        ("Which data type stores only unique elements?",
         "set", ["list", "tuple", "dict"]),
        ("How do you create an empty list in Python?",
         "[]", ["()", "{}", "<>"]),
        ("What is the output of bool(0) ?",
         "False", ["True", "0", "None"]),
        ("What does type(10) return?",
         "<class 'int'>", ["<class 'float'>", "<class 'str'>", "<class 'num'>"]),
    ],
    "Functions": [
        ("Which keyword is used to define a function in Python?",
         "def", ["func", "function", "define"]),
        ("Which keyword is used to send a value back from a function?",
         "return", ["give", "send", "output"]),
        ("A function that calls itself is called:",
         "Recursion", ["Iteration", "Looping", "Nesting"]),
        ("What is *args used for in a function?",
         "Passing a variable number of arguments", ["Passing only one argument",
                                                    "Passing a dictionary only",
                                                    "Returning many values"]),
        ("What does a function return if it has no return statement?",
         "None", ["0", "False", "Error"]),
        ("What is a lambda function?",
         "A small anonymous function", ["A function with a loop",
                                         "A built-in module",
                                         "A type of class"]),
        ("What is the output of: def add(a, b): return a + b ; print(add(2, 3)) ?",
         "5", ["23", "6", "Error"]),
        ("Which keyword lets a function change a global variable?",
         "global", ["static", "public", "extern"]),
        ("In def f(x=5), what is x=5 called?",
         "A default argument", ["A keyword argument", "A required argument", "A global argument"]),
    ],
    "Strings and Lists": [
        ("What is the output of 'Python'[0] ?",
         "P", ["y", "n", "Error"]),
        ("What does 'hello'.upper() return?",
         "HELLO", ["Hello", "hello", "hELLO"]),
        ("What does the append() method of a list do?",
         "Adds an item at the end", ["Adds an item at the start",
                                      "Removes the last item",
                                      "Sorts the list"]),
        ("What is the output of len('Python') ?",
         "6", ["5", "7", "Error"]),
        ("How do you access the last item of a list called a ?",
         "a[-1]", ["a[last]", "a[0]", "a[len]"]),
        ("Which method removes spaces from both ends of a string?",
         "strip()", ["trim()", "cut()", "remove()"]),
        ("What is the output of 'a,b,c'.split(',') ?",
         "['a', 'b', 'c']", ["'abc'", "('a','b','c')", "['a,b,c']"]),
        ("Which list method removes and returns the last item?",
         "pop()", ["remove()", "delete()", "clear()"]),
        ("What is the output of [1, 2, 3] + [4] ?",
         "[1, 2, 3, 4]", ["[5, 6, 7]", "[1, 2, 3, [4]]", "Error"]),
    ],
    "Loops and Conditions": [
        ("Which loop is best when the number of repetitions is known?",
         "for loop", ["while loop", "do-while loop", "if loop"]),
        ("What does range(1, 5) generate?",
         "1 2 3 4", ["1 2 3 4 5", "0 1 2 3 4", "2 3 4 5"]),
        ("Which keyword stops a loop immediately?",
         "break", ["stop", "exit", "continue"]),
        ("Which keyword skips the current iteration of a loop?",
         "continue", ["break", "pass", "skip"]),
        ("Which keyword is used for 'else if' in Python?",
         "elif", ["elseif", "else if", "elsif"]),
        ("How many times does 'for i in range(5):' run?",
         "5", ["4", "6", "0"]),
        ("Which of these is a logical operator in Python?",
         "and", ["&&", "||", "AND"]),
        ("Which statement is used as a placeholder that does nothing?",
         "pass", ["null", "skip", "none"]),
        ("What is the output of 5 == 5.0 ?",
         "True", ["False", "Error", "None"]),
    ],
    "OOP": [
        ("Which keyword is used to create a class?",
         "class", ["object", "def", "struct"]),
        ("What is the name of the constructor method in Python?",
         "__init__", ["__start__", "__new_object__", "constructor"]),
        ("What does 'self' refer to in a class method?",
         "The current object", ["The class name", "The parent class", "A global variable"]),
        ("What is inheritance?",
         "A child class getting the properties of a parent class",
         ["Copying a file", "Hiding data", "Creating many objects at once"]),
        ("What is an object?",
         "An instance of a class", ["A function", "A module", "A variable type"]),
        ("Wrapping data and methods together in one unit is called:",
         "Encapsulation", ["Polymorphism", "Recursion", "Inheritance"]),
        ("Using the same method name with different behaviour is called:",
         "Polymorphism", ["Inheritance", "Encapsulation", "Recursion"]),
        ("How do you make class B inherit from class A?",
         "class B(A):", ["class B inherits A:", "class B -> A:", "class A(B):"]),
    ],
    "Files, Modules and Errors": [
        ("Which function is used to open a file in Python?",
         "open()", ["file()", "read()", "load()"]),
        ("Which mode is used to open a file for writing?",
         "'w'", ["'r'", "'x'", "'o'"]),
        ("Which keyword is used to include a module in a program?",
         "import", ["include", "using", "load"]),
        ("Which module is used to work with JSON data?",
         "json", ["jsn", "data", "dict"]),
        ("Which statement closes a file automatically after use?",
         "with", ["close", "auto", "using"]),
        ("Which module is used to generate random numbers?",
         "random", ["rand", "math", "numbers"]),
        ("What does opening a file in 'a' mode do?",
         "Adds data at the end of the file", ["Deletes old data",
                                               "Reads the file only",
                                               "Creates a copy"]),
        ("Which block is used to handle an error in Python?",
         "except", ["catch", "error", "handle"]),
        ("Which error occurs when int('abc') is executed?",
         "ValueError", ["TypeError", "NameError", "SyntaxError"]),
        ("Which error is raised when a file that does not exist is opened for reading?",
         "FileNotFoundError", ["ValueError", "IndexError", "KeyError"]),
    ],
}


def build_sample_questions():
    """Convert SAMPLE_DATA into the format used in questions.json.
    The correct answer is placed at a different position each time
    (1, 2, 3, 4, 1, 2 ...) so it is not always the same option."""
    questions = []
    count = 0
    for category, items in SAMPLE_DATA.items():
        for text, correct, wrong in items:
            position = count % 4
            options = list(wrong)
            options.insert(position, correct)
            questions.append({
                "category": category,
                "question": text,
                "options": options,
                "answer": position + 1,
            })
            count += 1
    return questions


# ---------------------------------------------------------------
# File handling
# ---------------------------------------------------------------
def load_data(filename):
    """Read a list from a JSON file. Returns an empty list if the
    file does not exist yet or is empty or damaged."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_data(filename, data):
    """Write a list to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_sample_questions():
    """Add the sample questions to the bank. Questions that are already
    present (same question text) are skipped. Returns how many were added."""
    questions = load_data(QUESTIONS_FILE)
    existing = {q["question"].strip().lower() for q in questions}

    added = 0
    for q in build_sample_questions():
        if q["question"].strip().lower() not in existing:
            questions.append(q)
            added += 1

    save_data(QUESTIONS_FILE, questions)
    return added


def create_default_questions():
    """On the very first run (no questions yet) fill the bank with samples."""
    if not load_data(QUESTIONS_FILE):
        load_sample_questions()


# ---------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------
def get_number(prompt, low, high):
    """Keep asking until the user enters a whole number between
    low and high (both included)."""
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f"Please enter a number between {low} and {high}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def confirm(prompt):
    """Ask a yes/no question. Returns True for yes."""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


def get_category(q):
    """Old questions may not have a category, so use a default."""
    return q.get("category", "General")


def list_categories(questions):
    """Return the sorted list of categories present in the question bank."""
    return sorted({get_category(q) for q in questions})


# ---------------------------------------------------------------
# Login
# ---------------------------------------------------------------
def login():
    """Check the admin username and password. Returns True or False."""
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login successful.")
        return True
    print("Wrong username or password.")
    return False


# ---------------------------------------------------------------
# Admin functions
# ---------------------------------------------------------------
def choose_category_for_new_question(questions):
    """Let the admin pick an existing category or type a new one."""
    categories = list_categories(questions)
    print("\nChoose a category:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    new_option = len(categories) + 1
    print(f"  {new_option}. Create a new category")

    choice = get_number("Enter choice: ", 1, new_option)
    if choice == new_option:
        name = input("New category name: ").strip()
        return name if name else "General"
    return categories[choice - 1]


def add_question():
    questions = load_data(QUESTIONS_FILE)

    text = input("Enter the question: ").strip()
    if text == "":
        print("Question cannot be empty.")
        return

    # do not allow the same question twice
    for q in questions:
        if q["question"].strip().lower() == text.lower():
            print("This question already exists.")
            return

    options = []
    for i in range(1, 5):
        opt = input(f"Option {i}: ").strip()
        if opt == "":
            print("Option cannot be empty. Question not added.")
            return
        options.append(opt)

    if len(set(o.lower() for o in options)) < 4:
        print("All four options must be different. Question not added.")
        return

    answer = get_number("Correct option number (1-4): ", 1, 4)
    category = choose_category_for_new_question(questions)

    questions.append({
        "category": category,
        "question": text,
        "options": options,
        "answer": answer,
    })
    save_data(QUESTIONS_FILE, questions)
    print(f"Question added to '{category}'. Total questions: {len(questions)}")


def view_questions(detailed=True):
    """Show all questions with their numbers. If detailed is False only
    the question text is shown (useful before deleting)."""
    questions = load_data(QUESTIONS_FILE)
    if not questions:
        print("No questions available.")
        return

    print(f"\n--- Question Bank ({len(questions)} questions) ---")
    for category in list_categories(questions):
        print(f"\n[{category}]")
        for number, q in enumerate(questions, 1):
            if get_category(q) != category:
                continue
            print(f"Q{number}. {q['question']}")
            if detailed:
                for i, opt in enumerate(q["options"], 1):
                    print(f"     {i}. {opt}")
                print(f"     Correct answer: {q['answer']}")


def delete_question():
    questions = load_data(QUESTIONS_FILE)
    if not questions:
        print("No questions to delete.")
        return

    view_questions(detailed=False)
    number = get_number(f"\nEnter question number to delete (1-{len(questions)}): ",
                        1, len(questions))

    if confirm(f"Delete Q{number}?"):
        removed = questions.pop(number - 1)
        save_data(QUESTIONS_FILE, questions)
        print(f"Deleted: {removed['question']}")
    else:
        print("Nothing deleted.")


def show_question_summary():
    """Show how many questions each category has."""
    questions = load_data(QUESTIONS_FILE)
    if not questions:
        print("No questions available.")
        return

    print("\n--- Questions per Category ---")
    for category in list_categories(questions):
        count = sum(1 for q in questions if get_category(q) == category)
        print(f"{category:<30}{count}")
    print("-" * 35)
    print(f"{'Total':<30}{len(questions)}")


def clear_results():
    if not load_data(RESULTS_FILE):
        print("There are no results to clear.")
        return
    if confirm("This will delete ALL saved results. Continue?"):
        save_data(RESULTS_FILE, [])
        print("All results cleared.")
    else:
        print("Nothing deleted.")


def admin_menu():
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Add question")
        print("2. View all questions")
        print("3. Delete question")
        print("4. Questions per category")
        print("5. Load sample questions")
        print("6. View student results")
        print("7. Clear all results")
        print("8. Back to main menu")
        choice = get_number("Enter choice: ", 1, 8)

        if choice == 1:
            add_question()
        elif choice == 2:
            view_questions()
        elif choice == 3:
            delete_question()
        elif choice == 4:
            show_question_summary()
        elif choice == 5:
            added = load_sample_questions()
            print(f"{added} new sample questions added.")
        elif choice == 6:
            show_results()
        elif choice == 7:
            clear_results()
        else:
            break


# ---------------------------------------------------------------
# Student functions
# ---------------------------------------------------------------
def choose_quiz_category(questions):
    """Student picks a category or 'All categories'.
    Returns the category name, or None for all."""
    categories = list_categories(questions)
    print("\nChoose a category:")
    for i, cat in enumerate(categories, 1):
        count = sum(1 for q in questions if get_category(q) == cat)
        print(f"  {i}. {cat} ({count} questions)")
    all_option = len(categories) + 1
    print(f"  {all_option}. All categories ({len(questions)} questions)")

    choice = get_number("Enter choice: ", 1, all_option)
    if choice == all_option:
        return None
    return categories[choice - 1]


def get_grade(percentage):
    """Return a small remark for the score."""
    if percentage >= 90:
        return "Excellent"
    if percentage >= 75:
        return "Very Good"
    if percentage >= 60:
        return "Good"
    if percentage >= 40:
        return "Average"
    return "Needs more practice"


def take_quiz(name):
    """Run a random quiz. Returns (category, score, total) or None."""
    questions = load_data(QUESTIONS_FILE)
    if not questions:
        print("No questions available. Ask the admin to add some.")
        return None

    category = choose_quiz_category(questions)
    if category is None:
        pool = questions
        category_name = "All categories"
    else:
        pool = [q for q in questions if get_category(q) == category]
        category_name = category

    count = get_number(f"How many questions do you want? (1-{len(pool)}): ",
                       1, len(pool))

    # random.sample gives a random selection in a random order
    selected = random.sample(pool, count)

    print(f"\nStarting quiz on '{category_name}' with {count} questions.")
    print("Type the number of the option you think is correct.")

    score = 0
    wrong_answers = []

    for number, q in enumerate(selected, 1):
        # shuffle the options too, so the order changes every time
        correct_text = q["options"][q["answer"] - 1]
        options = q["options"][:]
        random.shuffle(options)
        correct_number = options.index(correct_text) + 1

        print(f"\nQ{number}/{count}. {q['question']}")
        for i, opt in enumerate(options, 1):
            print(f"   {i}. {opt}")

        choice = get_number("Your answer (1-4): ", 1, 4)
        if choice == correct_number:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. The correct answer is: {correct_text}")
            wrong_answers.append({
                "question": q["question"],
                "yours": options[choice - 1],
                "correct": correct_text,
            })

    # final result
    percentage = round(score / count * 100, 1)
    print("\n" + "=" * 40)
    print(f"{name}, you scored {score}/{count} ({percentage}%)")
    print(f"Remark: {get_grade(percentage)}")
    print("=" * 40)

    if wrong_answers:
        print("\n--- Questions you got wrong ---")
        for w in wrong_answers:
            print(f"\n{w['question']}")
            print(f"  Your answer   : {w['yours']}")
            print(f"  Correct answer: {w['correct']}")

    return category_name, score, count


def save_result(name, category, score, total):
    results = load_data(RESULTS_FILE)
    results.append({
        "name": name,
        "category": category,
        "score": score,
        "total": total,
        "percentage": round(score / total * 100, 1),
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
    })
    save_data(RESULTS_FILE, results)


def get_percentage(r):
    """Works for old results that did not store the percentage."""
    if "percentage" in r:
        return r["percentage"]
    return round(r["score"] / r["total"] * 100, 1) if r["total"] else 0


def show_results():
    results = load_data(RESULTS_FILE)
    if not results:
        print("No results saved yet.")
        return

    print("\n--- Saved Results ---")
    print(f"{'Name':<15}{'Category':<27}{'Score':<9}{'%':<8}{'Date'}")
    print("-" * 75)
    for r in results:
        score_text = f"{r['score']}/{r['total']}"
        print(f"{r['name']:<15}{r.get('category', 'All categories'):<27}"
              f"{score_text:<9}{get_percentage(r):<8}{r['date']}")


def show_leaderboard():
    results = load_data(RESULTS_FILE)
    if not results:
        print("No results saved yet.")
        return

    # highest percentage first, then higher number of questions
    ranked = sorted(results, key=lambda r: (get_percentage(r), r["total"]),
                    reverse=True)[:5]

    print("\n--- Top 5 Scores ---")
    print(f"{'Rank':<6}{'Name':<15}{'Category':<27}{'Score':<9}{'%'}")
    print("-" * 65)
    for rank, r in enumerate(ranked, 1):
        score_text = f"{r['score']}/{r['total']}"
        print(f"{rank:<6}{r['name']:<15}{r.get('category', 'All categories'):<27}"
              f"{score_text:<9}{get_percentage(r)}")


def student_menu():
    name = input("Enter your name: ").strip()
    if name == "":
        print("Name cannot be empty.")
        return

    result = take_quiz(name)
    if result:
        category, score, total = result
        save_result(name, category, score, total)
        print("\nYour result has been saved.")


# ---------------------------------------------------------------
# Main program
# ---------------------------------------------------------------
def main():
    create_default_questions()

    while True:
        print("\n===== QUIZ MANAGEMENT SYSTEM =====")
        print("1. Admin Login")
        print("2. Student - Take Quiz")
        print("3. View Results")
        print("4. Leaderboard (Top 5)")
        print("5. Exit")
        choice = get_number("Enter choice: ", 1, 5)

        if choice == 1:
            if login():
                admin_menu()
        elif choice == 2:
            student_menu()
        elif choice == 3:
            show_results()
        elif choice == 4:
            show_leaderboard()
        else:
            print("Thank you for using the Quiz Management System.")
            break


if __name__ == "__main__":
    main()