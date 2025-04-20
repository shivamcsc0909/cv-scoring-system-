import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()
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
