import pdfplumber
import re
from skills import SKILLS
from bs4 import BeautifulSoup


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def clean_text(text):

    # Remove HTML properly
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()

    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    return text


def extract_skills(text):
    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return list(set(found))
