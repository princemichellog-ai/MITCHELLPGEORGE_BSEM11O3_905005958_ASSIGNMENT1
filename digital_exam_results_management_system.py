"""
PROG211 - Object-Oriented Programming 1
Digital Exam & Results Management System (Education Domain)

WHAT THIS SYSTEM ACTUALLY DOES
-------------------------------
A real "digital exam" system has two halves:
  1. ADMINISTERING an exam  -> questions, options, a correct answer, auto-grading.
  2. MANAGING results       -> storing scores, computing grades/averages,
                                looking students up, reviewing history.

An examiner creates an Exam made of Question objects, a Student "sits" the
exam by answering, the system auto-grades it into a Result, and that Result
is stored against the Student for the rest of this session. The system
starts completely empty every run - no fake/demo records, and nothing is
written to disk."""

import datetime

# Tuple: fixed, never-changing reference data for converting a percentage
# into a letter grade.
GRADE_BOUNDARIES = (
    ("A", 80),
    ("B", 70),
    ("C", 60),
    ("D", 50),
    ("F", 0),
)


def score_to_grade(percentage):
    for letter, minimum in GRADE_BOUNDARIES:
        if percentage >= minimum:
            return letter
    return "F"


class Question:
    """One multiple-choice question belonging to an Exam."""

    def __init__(self, text, options, correct_index):
        self.text = text
        self.options = options              # list of option strings
        self.correct_index = correct_index  # index (0-based) of correct option

    def is_correct(self, chosen_index):
        return chosen_index == self.correct_index

    def display(self, number):
        print(f"\n Q{number}. {self.text}")
        for i, opt in enumerate(self.options):
            print(f"    {i + 1}. {opt}")


class Exam:
    """A named exam made up of several Question objects."""

    total_exams = 0  # class attribute: how many Exam objects exist

    def __init__(self, code, subject):
        self.code = code        # the exam's own ID, e.g. "EX-MATH01"
        self.subject = subject  # e.g. "Mathematics"
        self.questions = []     # list of Question objects
        Exam.total_exams += 1

    def add_question(self, question):
        self.questions.append(question)

    def total_marks(self):
        return len(self.questions)

    def grade(self, answers):
        """answers: list of chosen option indices, one per question."""
        score = 0
        for question, chosen in zip(self.questions, answers):
            if question.is_correct(chosen):
                score += 1
        return score, self.total_marks()

    @classmethod
    def get_total_exams(cls):
        return cls.total_exams


class Result:
    """The outcome of one student sitting one exam."""

    def __init__(self, exam, score, total):
        self.exam_code = exam.code
        self.subject = exam.subject
        self.score = score
        self.total = total
        self.percentage = round((score / total) * 100, 1) if total else 0
        self.grade = score_to_grade(self.percentage)
        self.date = datetime.date.today().isoformat()

    def display(self):
        print(f"   [{self.date}] {self.exam_code} ({self.subject}): "
              f"{self.score}/{self.total} = {self.percentage}% (Grade {self.grade})")


class Student:
    """Represents one student and the exam results they accumulate."""

    total_students = 0  # class attribute shared by every instance

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.results = []  # list of Result objects
        Student.total_students += 1

    def take_exam(self, exam, answers):
        score, total = exam.grade(answers)
        result = Result(exam, score, total)
        self.results.append(result)
        return result

    def calculate_average(self):
        if not self.results:
            return 0
        total = sum(r.percentage for r in self.results)
        return round(total / len(self.results), 1)

    def display_info(self):
        print(f"\nStudent: {self.name} (ID: {self.student_id})")
        if not self.results:
            print("   No exams sat yet.")
        else:
            for r in self.results:
                r.display()
            print(f"   Average: {self.calculate_average()}% "
                  f"(Overall grade: {score_to_grade(self.calculate_average())})")

    @classmethod
    def get_total_students(cls):
        return cls.total_students


# Data structure: dictionaries keyed by ID
students = {}   # student_id -> Student
exams = {}      # exam_code  -> Exam


def add_student(student):
    students[student.student_id] = student


def add_exam(exam):
    exams[exam.code] = exam


def display_all_students():
    print("\n===== ALL STUDENT RESULTS =====")
    if not students:
        print("No students registered yet.")
        return
    for s in students.values():
        s.display_info()


def get_non_empty_input(prompt):
    """Keep asking until the user actually types something (not just Enter)."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This can't be left empty. Please enter a value.")


def menu_register_student():
    sid = get_non_empty_input("New student ID (e.g. S003): ")
    if sid in students:
        print("That student ID already exists.")
        return
    name = get_non_empty_input("Student name: ")
    add_student(Student(sid, name))
    print(f"Registered {name} ({sid}).")


def menu_create_exam():
    code = get_non_empty_input("New exam code (e.g. EX-ENG01): ")
    if code in exams:
        print("That exam code already exists.")
        return
    subject = get_non_empty_input("Subject: ")
    exam = Exam(code, subject)

    try:
        n = int(input("How many questions? "))
    except ValueError:
        print("Invalid number.")
        return
    if n < 1:
        print("An exam needs at least 1 question.")
        return

    for i in range(n):
        text = get_non_empty_input(f"Question {i + 1} text: ")
        options = []
        for j in range(4):
            options.append(get_non_empty_input(f"  Option {j + 1}: "))

        # Keep asking until a valid 1-4 option number is given.
        while True:
            try:
                correct = int(input("  Correct option number (1-4): ")) - 1
                if 0 <= correct <= 3:
                    break
                print("  Please enter a number from 1 to 4.")
            except ValueError:
                print("  Please enter a number from 1 to 4.")

        exam.add_question(Question(text, options, correct))

    add_exam(exam)
    print(f"Exam {code} created with {n} question(s).")


def menu_take_exam():
    sid = get_non_empty_input("Student ID: ")
    student = students.get(sid)
    if not student:
        print("No such student.")
        return

    code = get_non_empty_input("Exam code: ")
    exam = exams.get(code)
    if not exam:
        print("No such exam.")
        return

    answers = []
    for i, q in enumerate(exam.questions, start=1):
        q.display(i)
        try:
            choice = int(input(" Your answer (option number): ")) - 1
        except ValueError:
            choice = -1
        answers.append(choice)

    result = student.take_exam(exam, answers)
    print(f"\nResult: {result.score}/{result.total} "
          f"({result.percentage}%) - Grade {result.grade}")


def menu_view_student():
    sid = get_non_empty_input("Student ID: ")
    student = students.get(sid)
    if not student:
        print("No such student.")
        return
    student.display_info()


def main_menu():
    while True:
        print("\n===== DIGITAL EXAM & RESULTS MANAGEMENT SYSTEM =====")
        print("1. Register a new student")
        print("2. Create a new exam")
        print("3. Take an exam (auto-graded)")
        print("4. View one student's results")
        print("5. View ALL students' results")
        print("6. View system stats")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            menu_register_student()
        elif choice == "2":
            menu_create_exam()
        elif choice == "3":
            menu_take_exam()
        elif choice == "4":
            menu_view_student()
        elif choice == "5":
            display_all_students()
        elif choice == "6":
            print(f"\nTotal students registered: {Student.get_total_students()}")
            print(f"Total exams created: {Exam.get_total_exams()}")
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu()