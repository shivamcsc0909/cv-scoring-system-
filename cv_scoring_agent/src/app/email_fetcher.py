import imaplib
import email
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch email credentials from the .env file
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")

# Directory to store fetched resumes
RESUME_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "resumes")
os.makedirs(RESUME_DIR, exist_ok=True)

def fetch_resumes():
    try:
        # Connect to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        # Search for unread emails
        status, messages = mail.search(None, '(UNSEEN)')
        if status != "OK":
            print("No unread emails found.")
            return

        for num in messages[0].split():
            status, msg_data = mail.fetch(num, '(RFC822)')
            if status != "OK":
                continue

            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)

            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                filename = part.get_filename()
                if filename:
                    filepath = os.path.join(RESUME_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Resume {filename} saved.")
        mail.logout()
    except Exception as e:
        print(f"Error fetching emails: {e}")

# Call this function to fetch resumes
fetch_resumes()
