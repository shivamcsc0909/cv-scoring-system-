def send_feedback_email(to_email, name, score_dict):
    # format email using template
    # send via SMTP securely
Hello {name},

Thank you for submitting your resume.

Here’s your score:
- Education: {education}
- Skills: {skills}
...

#from email_feedback import log_resume_score
#log_resume_score("cv1.pdf", 87)


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
