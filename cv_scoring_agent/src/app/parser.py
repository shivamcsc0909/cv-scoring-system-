import os
import re
import docx
import PyPDF2
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """PDF फाइल से टेक्स्ट एक्सट्रैक्ट करता है"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return ""

def extract_text_from_docx(docx_path):
    """DOCX फाइल से टेक्स्ट एक्सट्रैक्ट करता है"""
    try:
        doc = docx.Document(docx_path)
        return '\n'.join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from DOCX {docx_path}: {e}")
        return ""

def extract_contact_info(text):
    """रेज्यूमे टेक्स्ट से कॉन्टैक्ट इनफॉर्मेशन एक्सट्रैक्ट करता है"""
    # नाम का पैटर्न (आम तौर पर पहली लाइन)
    name = text.strip().split('\n')[0].strip() if text else "Unknown"
    
    # ईमेल एक्सट्रैक्ट करें
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    email = email_match.group(0) if email_match else "unknown@example.com"
    
    # फोन नंबर एक्सट्रैक्ट करें
    phone_match = re.search(r'(?:\+\d{1,3}[-\s]?)?\d{10}|(?:\d{3}[-\s]?){3}', text)
    phone = phone_match.group(0) if phone_match else "Unknown"
    
    return {
        "name": name,
        "email": email,
        "phone": phone
    }

def extract_experience_years(text):
    """Work experience के सालों को अनुमानित करता है"""
    # Experience सेक्शन की खोज करें
    experience_section = re.search(r'(?:EXPERIENCE|Experience|WORK|Work)[\s\S]+?(?:EDUCATION|Education|PROJECTS|Projects|SKILLS|Skills|$)', text)
    
    if experience_section:
        # एक्सपीरिएंस टेक्स्ट में सालों की खोज
        years_match = re.findall(r'(\d+)[\+]?\s*(?:year|yr)s?', experience_section.group(0), re.IGNORECASE)
        if years_match:
            return max([int(y) for y in years_match])
    
    # डेट्स से अनुमान लगाएं
    date_patterns = re.findall(r'(20\d\d)\s*[-–]\s*(20\d\d|Present|present|Current|current)', text)
    if date_patterns:
        years = 0
        for start, end in date_patterns:
            start_year = int(start)
            end_year = 2024 if end.lower() in ['present', 'current'] else int(end)
            years += (end_year - start_year)
        return years
    
    return 0

def parse_resume(file_path):
    """रेज्यूमे फाइल पार्स करता है और रिलेवेंट डेटा रिटर्न करता है"""
    if not os.path.exists(file_path):
        return None, f"File not found: {file_path}"
        
    try:
        # फाइल टाइप के अनुसार टेक्स्ट एक्सट्रैक्ट करें
        if file_path.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            return None, "Unsupported file format"
            
        if not text:
            return None, "No text could be extracted"
            
        # कॉन्टैक्ट इनफॉर्मेशन एक्सट्रैक्ट करें
        contact_info = extract_contact_info(text)
        
        # अनुभव के वर्षों का अनुमान लगाएं
        years_experience = extract_experience_years(text)
        
        return {
            "text": text,
            "name": contact_info["name"],
            "email": contact_info["email"],
            "phone": contact_info["phone"],
            "years_experience": years_experience,
            "file_name": os.path.basename(file_path)
        }, None
        
    except Exception as e:
        return None, f"Error parsing resume: {str(e)}"

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file from the root

email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")
openai_key = os.getenv("OPENAI_API_KEY")
