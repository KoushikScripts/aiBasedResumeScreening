import fitz
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from utils.feature_extractor import extract_features

app = Flask(__name__)
model = joblib.load("model/resume_score_model.pkl")

def extract_text_from_pdf_bytes(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

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

    features = pd.DataFrame([extract_features(raw_text)])
    score = model.predict(features)[0]

    improvements = {
        'handled': 'managed',
        'worked on': 'developed',
        'responsible for': 'led',
        'helped': 'contributed to',
        'tasked with': 'spearheaded'
    }
    word_replacements = {k: v for k, v in improvements.items() if k in raw_text.lower()}

    missing_sections = []
    if 'certification' not in raw_text.lower():
        missing_sections.append('Certifications')
    if 'project' not in raw_text.lower():
        missing_sections.append('Projects')
    if 'summary' not in raw_text.lower():
        missing_sections.append('Summary')

    feedback = []
    if len(raw_text.split()) < 150:
        feedback.append("Add more detail to expand resume content")
    if not word_replacements:
        feedback.append("Use more powerful action verbs")

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
