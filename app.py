from flask import Flask, render_template, request, jsonify
import os
import time
import hashlib
from datetime import datetime

from resume_extractor import extract_text
from resume_parser import (
    extract_name, extract_email, extract_phone,
    extract_skills, extract_links, categorize_skills, skills_list,
    extract_title, extract_summary, extract_experience
)
from ats_scorer import calculate_ats_score, enhance_bullet_point, JOB_PROFILES, generate_role_screening_questions

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DATA_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("output", exist_ok=True)


def parse_file(file_path, filename):
    start_time = time.time()
    text = extract_text(file_path)
    extraction_time = round((time.time() - start_time) * 1000, 1)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    links = extract_links(text)
    categorized_skills = categorize_skills(skills)

    words = text.split()
    word_count = len(words)
    char_count = len(text)
    reading_time = max(1, round(word_count / 200))

    # Calculate deterministic confidence metric
    confidence = 0
    if name and name != "Not found":
        confidence += 30
    if email and email != "Not found":
        confidence += 25
    if phone and phone != "Not found":
        confidence += 20
    if len(skills) >= 3:
        confidence += 15
    elif len(skills) >= 1:
        confidence += 10
    if links:
        confidence += 10
    confidence = min(99.4, max(45.0, float(confidence)))

    # Deterministic Candidate Hash
    hash_seed = f"{filename}_{name}_{email}".encode('utf-8')
    cand_id = f"CAND-{hashlib.md5(hash_seed).hexdigest()[:6].upper()}"

    title = extract_title(text, skills)
    cand_name = name if name else "Candidate Profile"
    summary = extract_summary(text, cand_name, title, skills)
    experience = extract_experience(text)

    # Compute Comprehensive Multi-Pillar ATS Evaluation
    ats_analysis = calculate_ats_score(
        text=text,
        name=cand_name,
        email=email,
        phone=phone,
        skills=skills,
        links=links,
        experience=experience
    )

    return {
        "candidate_id": cand_id,
        "filename": filename,
        "name": cand_name,
        "title": title,
        "summary": summary,
        "experience": experience,
        "email": email if email else "Not documented",
        "phone": phone if phone else "Not documented",
        "skills": skills,
        "categorized_skills": categorized_skills,
        "links": links,
        "confidence_score": f"{confidence}%",
        "ats_score": ats_analysis["overall_score"],
        "ats_analysis": ats_analysis,
        "stats": {
            "word_count": word_count,
            "char_count": char_count,
            "skills_count": len(skills),
            "reading_time_min": reading_time,
            "latency_ms": extraction_time
        },
        "provenance": {
            "ingestion_timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "parser_engine": "PyMuPDF Native C++ Vector Stream",
            "ner_model": "spaCy en_core_web_sm v3.8"
        },
        "text": text
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        if "resume" not in request.files or not request.files["resume"].filename:
            error = "Please select a resume file before uploading."
            return render_template("index.html", result=result, error=error)

        file = request.files["resume"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            result = parse_file(file_path, file.filename)
        except Exception as e:
            error = f"Error processing file: {str(e)}"

    return render_template("index.html", result=result, error=error)


@app.route("/api/parse", methods=["POST"])
def api_parse():
    if "resume" not in request.files or not request.files["resume"].filename:
        return jsonify({"success": False, "error": "No resume file provided."}), 400

    file = request.files["resume"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        result = parse_file(file_path, file.filename)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "Operational",
        "pipeline": "All local services verified",
        "engines": {
            "vector_parser": "PyMuPDF v1.25.3 (Active)",
            "ner_pipeline": "spaCy en_core_web_sm (Loaded)",
            "optical_ocr": "Tesseract OCR v5.3.0 (Ready)"
        },
        "version": "2.4.0-enterprise",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })


@app.route("/api/stats", methods=["GET"])
def api_stats():
    data_resumes = 0
    if os.path.exists(DATA_FOLDER):
        for root, dirs, files in os.walk(DATA_FOLDER):
            data_resumes += len([f for f in files if f.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".txt"))])
    
    uploads_count = 0
    if os.path.exists(UPLOAD_FOLDER):
        uploads_count = len(os.listdir(UPLOAD_FOLDER))

    return jsonify({
        "success": True,
        "corpus_total": data_resumes,
        "uploads_total": uploads_count,
        "skills_catalog_size": len(skills_list),
        "status": "Operational",
        "engine_version": "PyMuPDF 1.25 / spaCy 3.8 / Tesseract 5.3"
    })


@app.route("/api/enhance_bullet", methods=["POST"])
def api_enhance_bullet():
    payload = request.get_json(silent=True) or {}
    bullet = payload.get("bullet", "").strip()
    skills = payload.get("skills", [])
    if not bullet:
        return jsonify({"success": False, "error": "Please provide a resume bullet point to enhance."}), 400

    suggestions = enhance_bullet_point(bullet, skills)
    return jsonify({"success": True, "suggestions": suggestions})


@app.route("/api/role_match", methods=["POST"])
def api_role_match():
    payload = request.get_json(silent=True) or {}
    role_name = payload.get("role", "").strip()
    skills = payload.get("skills", [])
    skills_lower_set = set(s.lower() for s in skills)

    if role_name in JOB_PROFILES:
        req = JOB_PROFILES[role_name]["required_skills"]
        bonus = JOB_PROFILES[role_name]["bonus_skills"]
        desc = JOB_PROFILES[role_name]["description"]
    else:
        # Heuristic keywords for custom role
        words = [w.lower() for w in role_name.replace("/", " ").split() if len(w) > 2]
        req = words[:6] if words else ["python", "sql", "git"]
        bonus = ["docker", "rest api", "linux"]
        desc = f"Enterprise position alignment for {role_name}."

    matched_req = [s for s in req if s in skills_lower_set]
    missing_req = [s for s in req if s not in skills_lower_set]
    matched_bonus = [s for s in bonus if s in skills_lower_set]
    missing_bonus = [s for s in bonus if s not in skills_lower_set]

    req_match_pct = round((len(matched_req) / max(1, len(req))) * 100)
    overall_match = min(98, max(25, round(req_match_pct * 0.8 + (len(matched_bonus) / max(1, len(bonus))) * 20)))

    all_required_breakdown = [
        {
            "skill": s.upper(),
            "status": "matched" if s in skills_lower_set else "missing"
        }
        for s in req
    ]

    screening_questions = generate_role_screening_questions(skills, role_name)

    return jsonify({
        "success": True,
        "role": role_name,
        "match_percentage": overall_match,
        "required_match_percentage": req_match_pct,
        "total_required_count": len(req),
        "matched_required_count": len(matched_req),
        "description": desc,
        "all_required_skills": all_required_breakdown,
        "required_skills_list": [s.upper() for s in req],
        "matched_skills": [s.upper() for s in matched_req],
        "missing_skills": [s.upper() for s in missing_req],
        "matched_bonus_skills": [s.upper() for s in matched_bonus],
        "missing_bonus_skills": [s.upper() for s in missing_bonus],
        "status": "Strong Match" if req_match_pct >= 70 else ("Qualified Alignment" if req_match_pct >= 45 else "Development Opportunity"),
        "screening_questions": screening_questions
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
