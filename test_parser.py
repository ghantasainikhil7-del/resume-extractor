import os

from resume_extractor import extract_text
from resume_parser import extract_name, extract_email, extract_phone, extract_skills


resume_folder = "data"
resume_files = []

for root, dirs, files in os.walk(resume_folder):
    for file in files:
        if file.lower().endswith((".txt", ".pdf", ".jpg", ".jpeg", ".png")):
            resume_files.append(os.path.join(root, file))


for i, file_path in enumerate(resume_files[:2480]):  # testing first 10 resumes

    print("\n--------------------------------")
    print(f"Resume {i+1}: {file_path}")

    text = extract_text(file_path)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    print("Name:", name if name else "Not found")
    print("Email:", email if email else "Not found")
    print("Phone:", phone if phone else "Not found")
    print("Skills:", skills if skills else "Not found")