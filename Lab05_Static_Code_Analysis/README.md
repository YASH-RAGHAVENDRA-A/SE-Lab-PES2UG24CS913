# Lab 5 - Static Code Analysis

## Objective

Improve the quality, reliability and security of the loan eligibility
and EMI calculator using Pylint, Bandit and Flake8.

## Deliverables

- loan_calculator.py: corrected Python program
- issues.md: identified issues and fix approaches
- reflection.md: reflection answers
- requirements.txt: Python dependencies
- PES2UG24CS913_YashRaghavendraA_Lab05.pdf: submitted lab report
- reports/: original and final static-analysis reports

## Run the program

Use Python 3.10 or newer. Create and activate a virtual environment,
then install dependencies:

    python -m venv .venv
    python -m pip install -r requirements.txt

Compile the code:

    python -m py_compile loan_calculator.py

Run the demonstration:

    python loan_calculator.py

## Static analysis

Run the tools from the project directory:

    python -m pylint loan_calculator.py
    python -m bandit -r loan_calculator.py
    python -m flake8 loan_calculator.py

Original and final report files are stored in reports/.

The demonstration does not perform real SFTP uploads or send email.
Those functions require appropriately configured servers and credentials.
