import fitz  # PyMuPDF
import joblib
import pandas as pd
import re
from flask import Flask, request, jsonify
from utils.feature_extractor import extract_features

app = Flask(__name__)

# Load trained model
model = joblib.load("model/resume_score_model.pkl")

# Function to extract text from PDF bytes
def extract_text_from_pdf_bytes(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

@app.route('/predict', methods=['POST'])
def predict_from_uploaded_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        file_bytes = file.read()
        raw_text = extract_text_from_pdf_bytes(file_bytes)
    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {e}"}), 400

    try:
        features = pd.DataFrame([extract_features(raw_text)])
        score = model.predict(features)[0]
    except Exception as e:
        return jsonify({"error": f"Model prediction failed: {e}"}), 500

    # Improvement suggestions
    improvements = {
        'handled': 'managed',
        'worked on': 'developed',
        'responsible for': 'led',
        'helped': 'contributed to',
        'tasked with': 'spearheaded'
    }
    word_replacements = {k: v for k, v in improvements.items() if k in raw_text.lower()}

    # Check for missing sections
    missing_sections = []
    required_sections = ['certificates', 'project', 'education', 'experience', 'skills']
    for section in required_sections:
        if section not in raw_text.lower():
            missing_sections.append(section.capitalize())

    # Style & structure feedback
    feedback = []

    if len(raw_text.split()) < 150:
        feedback.append("Add more detail to expand resume content.")
    if not word_replacements:
        feedback.append("Use more powerful action verbs.")

    # Additional advanced checks
    if re.search(r'\bi\b', raw_text, re.IGNORECASE):
        feedback.append("Avoid using first-person pronouns like 'I'; resumes should be written in third person.")
    if raw_text.count('•') < 3:
        feedback.append("Consider using bullet points for better readability.")
    if len(raw_text.split('.')) < 10:
        feedback.append("Add more concise, impactful statements.")
    if "objective" in raw_text.lower():
        try:
            objective_part = raw_text.lower().split("objective")[1].split()
            if len(objective_part) < 10:
                feedback.append("Your career objective seems too brief — consider expanding it with a clearer goal.")
        except:
            pass
    if re.search(r'(hardworking|team player|self-motivated)', raw_text.lower()):
        feedback.append("Avoid overused buzzwords like 'hardworking' — focus on quantifiable results instead.")

    return jsonify({
        "score": round(score, 2),
        "suggestions": {
            "word_replacements": word_replacements,
            "missing_sections": missing_sections,
            "style_feedback": feedback
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
