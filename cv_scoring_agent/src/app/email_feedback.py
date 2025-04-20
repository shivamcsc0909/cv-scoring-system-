import logging
import os

# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "app.log")

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_resume_score(resume_name, score):
    """
    Logs the name and score of a resume.
    """
    logging.info(f"Resume: {resume_name} | Score: {score}")
