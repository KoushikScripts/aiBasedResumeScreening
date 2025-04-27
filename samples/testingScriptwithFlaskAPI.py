# bro some imports
from flask import Flask, send_file
import fitz  # pymupdf
import re
from pathlib import Path

# bro setup server
app = Flask(__name__)

# bro the function to process pdfs
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
    print(f"✅ Bro done! Highlighted PDF saved at: {output_pdf_path}")

# bro the api route
@app.route('/process-resume', methods=['GET'])
def process_resume_api():
    input_pdf_path = "/home/surya/Projects/aiResumeScreaning/data/sampleResume.pdf" # change this path to the actual path where you saved the sample resume file
    output_pdf_path = "/home/surya/Projects/aiResumeScreaning/data/highlighted_sampleResume.pdf" #change this path to where you want to download

    # bro check if file even exists lol
    if not Path(input_pdf_path).exists():
        return {"error": "Bruh! Input PDF not found 😭"}, 404

    process_and_highlight_pdf(input_pdf_path, output_pdf_path)

    return send_file(output_pdf_path, as_attachment=True)

# bro start the server
if __name__ == "__main__":
    app.run(debug=True)

    # after changing that you can just visit "http://localhost:5000/process-resume" to run the api which will fetch the pdf and hilight it with the errors
