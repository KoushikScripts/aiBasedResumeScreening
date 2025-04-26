from flask import Flask, request, send_file
import fitz  # PyMuPDF
import tempfile
import os

# --- your function copy paste ---
import re
from pathlib import Path

def process_and_highlight_pdf(input_pdf_path, output_pdf_path):
    doc = fitz.open(input_pdf_path)

    important_sections = ["Education", "Experience", "Skills", "Projects", "Certifications", "Contact", "Summary"]

    for page in doc:
        text = page.get_text()
        y_position = 50

        for section in important_sections:
            if section.lower() not in text.lower():
                page.insert_text(
                    (50, y_position),
                    f"⚠️ Missing Section: {section}",
                    fontsize=12,
                    color=(1, 0, 0)
                )
                y_position += 20

        if len(re.findall(r"\bI\b", text)) > 15:
            page.insert_text(
                (50, y_position + 30),
                "⚠️ Too much 'I' usage",
                fontsize=12,
                color=(1, 0, 0)
            )

    doc.save(output_pdf_path)
    print(f"✅ Done! Highlighted PDF saved as: {output_pdf_path}")

# --- Flask part starts here ---

app = Flask(__name__)

@app.route('/process-resume', methods=['POST'])
def process_resume():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files['file']

    if file.filename == '':
        return {"error": "Empty filename"}, 400

    # Save the uploaded file to a temporary location
    with tempfile.TemporaryDirectory() as tmpdirname:
        input_path = os.path.join(tmpdirname, 'input_resume.pdf')
        output_path = os.path.join(tmpdirname, 'highlighted_resume.pdf')

        file.save(input_path)

        # Process the uploaded PDF
        process_and_highlight_pdf(input_path, output_path)

        # Return the highlighted file
        return send_file(output_path, as_attachment=True, download_name='highlighted_resume.pdf')

if __name__ == '__main__':
    app.run(debug=True)
