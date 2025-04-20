# Automated CV Scoring and Feedback System

This AI-driven system parses, scores, and gives feedback on resumes based on a job description. Built with Python, optimized for simplicity and clarity.

## Features:
- Parses PDF/DOCX resumes
- Scores resumes using keyword & logic-based evaluation
- Sends feedback emails automatically
- Logs all activity in a CSV

## Folder Structure
- `app/` – All core logic
- `resumes/` – Drop your CVs here
- `logs/` – Stores logs of processed resumes
- `config/` – Central config for JD and email

## How to Run:
```bash
pip install -r requirements.txt
python app/main.py
