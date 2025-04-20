# app/utils.py
import os
import csv
import logging
import datetime
from app.config import LOG_FOLDER

# लॉगिंग सेटअप
def setup_logging():
    """लॉगिंग सेटअप करता है"""
    # लॉग फोल्डर बनाएं अगर नहीं है तो
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    
    # लॉग फाइल पाथ
    log_file = os.path.join(LOG_FOLDER, f"cv_processing_{datetime.datetime.now().strftime('%Y%m%d')}.log")
    
    # लॉगर कॉन्फ़िगर करें
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # कंसोल हैंडलर जोड़ें
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console)
    
    return logging.getLogger('')

def log_to_csv(resume_data, score_data, email_status):
    """CSV में प्रोसेस्ड रिज्यूम्स का रिकॉर्ड रखता है"""
    csv_file = os.path.join(LOG_FOLDER, f"processed_resumes_{datetime.datetime.now().strftime('%Y%m%d')}.csv")
    
    # फाइल नई है या नहीं चेक करें
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = [
            'Timestamp', 'Name', 'Email', 'File', 'Total Score', 
            'Education', 'Experience', 'Skills', 'Formatting', 'JD Match',
            'Email Status'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # अगर फाइल नई है तो हेडर लिखें
        if not file_exists:
            writer.writeheader()
        
        # रिज़ल्ट्स लिखें
        writer.writerow({
            'Timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Name': resume_data["name"],
            'Email': resume_data["email"],
            'File': resume_data["file_name"],
            'Total Score': score_data["total_score"],
            'Education': score_data["scores"]["Education"],
            'Experience': score_data["scores"]["Experience"],
            'Skills': score_data["scores"]["Skills"],
            'Formatting': score_data["scores"]["Formatting"],
            'JD Match': score_data["scores"]["JD Match"],
            'Email Status': "Sent" if email_status[0] else f"Failed: {email_status[1]}"
        })

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file from the root

email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")
openai_key = os.getenv("OPENAI_API_KEY")

import imaplib
import email
import os

def fetch_resumes():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')
    for num in messages[0].split():
        status, msg_data = mail.fetch(num, '(RFC822)')
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue
            filename = part.get_filename()
            if filename:
                filepath = os.path.join("resumes", filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
