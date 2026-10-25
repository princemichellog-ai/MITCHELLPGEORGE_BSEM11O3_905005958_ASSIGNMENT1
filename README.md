# MITCHELLPGEORGE_BSEM11O3_905005958_ASSIGNMENT1
DIGITAL EXAM AND RESULT MANAGEMENT SYSTEM
PROG211 - Object-Oriented Programming 1 (Education Domain)

A console program where a teacher creates multiple-choice exams and students sit them, with automatic grading and result tracking.

## How to Run
save file digital_exam_results_management_system.py
run the command below in terminal
```
python3 digital_exam_results_system.py
```

## Classes
- **Question** - one multiple-choice question
- **Exam** - a set of Questions, auto-grades answers
- **Result** - one student's outcome on one exam
- **Student** - a learner and their results over time

## Data Structure
Two dictionaries, keyed by ID: `students` and `exams`.

## DPG Alignment
- **Open-source**: published on GitHub
- **Privacy-respecting**: no real data; nothing saved to disk
- **Inclusive**: plain console program, no special requirements
- **Modular**: each class has one clear job, reusable elsewhere

## Note
Data is in-memory only and clears when the program exits.
