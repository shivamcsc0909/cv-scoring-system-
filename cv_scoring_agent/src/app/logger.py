import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

def log_resume_score(resume_name, score):
    logging.info(f"Resume: {resume_name}, Score: {score}")
