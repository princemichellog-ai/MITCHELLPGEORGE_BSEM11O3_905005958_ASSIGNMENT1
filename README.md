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
- *SDG Alignment*: This project supports *UN Sustainable Development Goal 4 (Quality Education)*, which calls for inclusive and equitable quality education for all. The system supports this goal by giving schools a free, open-source way to create exams, grade them automatically, and track student performance — without needing paid software, internet access, or specialized hardware. This makes it especially useful in under-resourced schools where access to digital assessment tools is limited, helping teachers save time on grading while giving students faster, more consistent feedback on their learning.

Want 

## Note
Data is in-memory only and clears when the program exits.
