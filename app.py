from flask import Flask, render_template, request
import os

from resume_extractor import extract_text
from resume_parser import extract_name, extract_email, extract_phone, extract_skills

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        file = request.files["resume"]

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        text = extract_text(file_path)

        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)

        result = {
            "name": name if name else "Not found",
            "email": email if email else "Not found",
            "phone": phone if phone else "Not found",
            "skills": skills,
            "text": text[:500]
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)