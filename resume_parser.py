import re
import spacy

# load NLP model
nlp = spacy.load("en_core_web_sm")


# ---------------- EMAIL (Regex) ----------------

def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    return match.group() if match else ""


# ---------------- PHONE (Regex) ----------------

def extract_phone(text):

    pattern = r"\+?\d[\d\s\-]{8,}\d"

    match = re.search(pattern, text)

    return match.group() if match else ""


# ---------------- NAME (spaCy NER) ----------------

banned_words = [
    "resume","summary","objective","skills",
    "experience","education","profile",
    "maintained","developed","managed",
    "ledger","excel","word","project"
]

def extract_name(text):

    lines = text.split("\n")[:8]        # check only top lines
    text_chunk = " ".join(lines)

    doc = nlp(text_chunk)

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            name = ent.text.strip()

            if name.lower() not in banned_words and 1 < len(name.split()) <= 3:
                return name

    return ""


# ---------------- SKILLS ----------------

skills_list = [
    "python","java","c++","sql","machine learning","deep learning",
    "nlp","data science","pandas","numpy","tensorflow",
    "pytorch","excel","power bi","tableau","aws","docker"
]

def extract_skills(text):

    text = text.lower()

    found = []

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    return list(set(found))