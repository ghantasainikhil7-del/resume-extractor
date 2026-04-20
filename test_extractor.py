import os
from resume_extractor import extract_text

resume_folder = "data"

resume_files = []

# Read all files including subfolders
for root, dirs, files in os.walk(resume_folder):
    for file in files:
        if file.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            resume_files.append(os.path.join(root, file))

print("Total resumes:", len(resume_files))


for i, file_path in enumerate(resume_files):

    print(f"\nProcessing {i+1}/{len(resume_files)} : {file_path}")

    text = extract_text(file_path)

    print(text[:500])
    print("EXTRACTED SUCCESFULLY")