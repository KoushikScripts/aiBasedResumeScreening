#  import stuff here
import fitz  # pymupdf library
import re
from pathlib import Path

# function to process pdfs
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
                (50, y_position + 30),to
                "⚠️ Too much 'I' usage",
                fontsize=12,
                color=(1, 0, 0)
            )

    doc.save(output_pdf_path)
    print(f"✅ Done! Highlighted PDF saved as: {output_pdf_path}")

if __name__ == "__main__":
    # bro change these paths to whatever you want
    input_pdf = "/home/surya/Projects/aiResumeScreaning/data/sampleResume.pdf"
    output_pdf = "/home/surya/Projects/aiResumeScreaning/data/highlighted_sampleResume.pdf"

    if Path(input_pdf).exists():
        process_and_highlight_pdf(input_pdf, output_pdf)
    else:
        print(f"Bruh! File {input_pdf} not found 😭")

