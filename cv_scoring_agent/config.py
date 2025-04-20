# app/config.py

# फोल्डर पाथ्स
RESUME_FOLDER = "./resumes"
LOG_FOLDER = "./logs"
TEMPLATE_FOLDER = "./templates"

# ईमेल कॉन्फिगरेशन
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your-app-password"  # Google App Password या वैसा ही
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# स्कोरिंग वेटेज
SCORING_WEIGHTS = {
    "Education": 20,
    "Experience": 20,
    "Skills": 20,
    "Formatting": 20,
    "JD Match": 20
}

# जॉब डिस्क्रिप्शन कीवर्ड्स (इन्हें जॉब रिक्वायरमेंट्स के हिसाब से एडिट करें)
JD_KEYWORDS = [
    "python", "ai", "ml", "machine learning", "developer", 
    "data analysis", "programming", "computer science"
]

# कीवर्ड बैंक (आवश्यकतानुसार एडिट करें)
KEYWORDS = {
    "ai": ["artificial intelligence", "machine learning", "deep learning", "AI", "ML", "NLP"],
    "languages": ["python", "java", "c++", "r language", "javascript"],
    "webdev": ["react", "node", "html", "css", "django", "flask"],
    "database": ["sql", "mysql", "mongodb", "postgresql"],
    "skills": ["data mining", "data cleaning", "scikit-learn", "tensorflow", "pandas"],
    "education": ["bca", "b.tech", "bachelor", "computer science", "engineering", "diploma"]
}

import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
