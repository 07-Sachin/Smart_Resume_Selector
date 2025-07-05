import fitz  # PyMuPDF
import os

def extract_resume_texts(filepaths):
    resume_data = []

    for path in filepaths:
        content = ''
        if path.lower().endswith('.pdf'):
            doc = fitz.open(path)
            for page in doc:
                content += page.get_text()
        elif path.lower().endswith('.txt'):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

        resume_data.append({'filename': os.path.basename(path), 'content': content})

    return resume_data
