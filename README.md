Quiz Management System

A console based quiz application written in Python. A teacher (admin) can manage a bank of multiple-choice questions, and students can take random quizzes, see their score instantly and have their results saved.

This project was made as a mini project for the Python Programming subject.

Features

Admin

Login with username and password
Add, view and delete questions
Organise questions into categories (or create a new category)
See how many questions each category has
Reload the built-in sample questions
View and clear student results

Student

Choose a category (or all categories) and the number of questions
Every quiz uses a random set of questions in a random order
The four options of each question are shuffled every time
Instant feedback after each answer
Final score, percentage and a remark (Excellent, Very Good, Good, Average, Needs more practice)
Review of the questions answered wrongly
Result saved with name, category, score and date

General

64 ready-made Python questions in 7 categories
Results table and a Top 5 leaderboard
Input validation, so wrong input never crashes the program
No database and no external library needed
Question Categories
Category	Questions
Python Basics	10
Data Types	9
Functions	9
Strings and Lists	9
Loops and Conditions	9
OOP	8
Files, Modules and Errors	10
Technologies Used
Python 3
Built-in modules only: json, random, os, datetime
Project Structure
quiz-management-system/
├── quiz_management_system.py   # the complete program
├── README.md                   # this file
├── questions.json              # created automatically on first run
└── results.json                # created automatically after the first quiz
How to Run
Make sure Python 3 is installed:
   python --version
Download or clone this repository:
   git clone https://github.com/<your-username>/quiz-management-system.git
   cd quiz-management-system
Run the program:
   python quiz_management_system.py

On the first run the question bank is created automatically with the sample questions.

Admin Login
Username	Password
admin	admin123

You can change these at the top of quiz_management_system.py (ADMIN_USERNAME and ADMIN_PASSWORD).

How It Works
The main menu offers Admin Login, Student quiz, View Results, Leaderboard and Exit.
When a student starts a quiz, the program loads the questions from questions.json.
random.sample() picks the chosen number of questions from the selected category, so every quiz is different.
random.shuffle() shuffles the options of each question. The program remembers the correct answer as text, so the right answer is still found after shuffling.
After the last question, the score and percentage are calculated and the result is saved in results.json.
Data format

A question in questions.json:

json
{
    "category": "Python Basics",
    "question": "Which function is used to display output on the screen?",
    "options": ["show()", "print()", "display()", "echo()"],
    "answer": 2
}

A result in results.json:

json
{
    "name": "Rahul",
    "category": "Python Basics",
    "score": 4,
    "total": 5,
    "percentage": 80.0,
    "date": "29-10-2026 06:03"
}
Sample Output
===== QUIZ MANAGEMENT SYSTEM =====
1. Admin Login
2. Student - Take Quiz
3. View Results
4. Leaderboard (Top 5)
5. Exit
Enter choice: 2
Enter your name: Rahul

Choose a category:
  1. Data Types (9 questions)
  2. Files, Modules and Errors (10 questions)
  3. Functions (9 questions)
  4. Loops and Conditions (9 questions)
  5. OOP (8 questions)
  6. Python Basics (10 questions)
  7. Strings and Lists (9 questions)
  8. All categories (64 questions)
Enter choice: 6
How many questions do you want? (1-10): 5

Q1/5. Which function is used to display output on the screen?
   1. display()
   2. show()
   3. echo()
   4. print()
Your answer (1-4): 4
Correct!

========================================
Rahul, you scored 4/5 (80.0%)
Remark: Very Good
========================================
Python Concepts Used
Functions
Lists and dictionaries
Loops and conditional statements
File handling with JSON
Exception handling (try / except)
The random and datetime modules
f-string formatting
Limitations
Console based, no graphical interface
The admin password is stored as plain text in the code
Only multiple-choice questions with four options
No time limit for the quiz
Data is stored locally, so it works on one computer only
Future Improvements
Graphical interface using Tkinter or a web version using Flask
SQLite database instead of JSON files
Timer for each quiz and difficulty levels
Password encryption and separate student accounts
Export results as a PDF or Excel file
