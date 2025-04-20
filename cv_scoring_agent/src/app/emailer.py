# app/emailer.py
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, TEMPLATE_FOLDER

def load_email_template():
    """ईमेल टेम्पलेट लोड करता है"""
    template_path = os.path.join(TEMPLATE_FOLDER, "email_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading email template: {e}")
        # बैकअप टेम्पलेट
        return """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Hello {name},</h2>
            <p>Thank you for submitting your resume. Here's your evaluation results:</p>
            
            <h3>Your Resume Score: {total_score}/100</h3>
            
            <h4>Score Breakdown:</h4>
            <ul>
                {score_breakdown}
            </ul>
            
            <h4>Feedback:</h4>
            <p>{feedback}</p>
            
            <p>Best regards,<br>Elint Recruitment Team</p>
        </body>
        </html>
        """

def format_email_content(candidate_data, score_data):
    """ईमेल कंटेंट फॉर्मेट करता है"""
    template = load_email_template()
    
    # स्कोर ब्रेकडाउन लिस्ट बनाएं
    score_breakdown = ""
    for category, score in score_data["scores"].items():
        score_breakdown += f"<li><strong>{category}:</strong> {score}/20</li>"
    
    # फीडबैक को HTML फॉर्मेट में कनवर्ट करें
    feedback_html = score_data["feedback"].replace("\n", "<br>")
    
    # प्लेसहोल्डर्स रिप्लेस करें
    email_content = template.format(
        name=candidate_data["name"],
        total_score=score_data["total_score"],
        score_breakdown=score_breakdown,
        feedback=feedback_html
    )
    
    return email_content

def send_feedback_email(candidate_data, score_data):
    """कैंडिडेट को फीडबैक ईमेल भेजता है"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Your Resume Evaluation - Score: {score_data['total_score']}/100"
        msg['From'] = EMAIL_SENDER
        msg['To'] = candidate_data["email"]
        
        # HTML कंटेंट फॉर्मेट करें
        html_content = format_email_content(candidate_data, score_data)
        msg.attach(MIMEText(html_content, 'html'))
        
        # ईमेल भेजें
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            
        return True, f"Email sent successfully to {candidate_data['email']}"
    
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file from the root

email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")
openai_key = os.getenv("OPENAI_API_KEY")
