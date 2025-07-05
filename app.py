from flask import Flask, render_template, request, send_from_directory
import os
from resumes.utils.resume_reader import extract_resume_texts
from resumes.utils.gemini_ranker import rank_resumes_with_gemini
from resumes.utils.generate_pdf_report import generate_pdf_report

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'resumes'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_description = request.form['job_description']
        files = request.files.getlist('resumes')

        filepaths = []
        for file in files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            filepaths.append(filepath)

        # Extract and rank resumes
        resume_texts = extract_resume_texts(filepaths)
        ranked = rank_resumes_with_gemini(job_description, resume_texts)

        # Save PDF report in root directory or 'static/' (optional)
        pdf_filename = "ranked_resumes.pdf"
        pdf_path = generate_pdf_report(ranked, output_path=pdf_filename)

        return render_template(
            'results.html',
            results=ranked,
            query=job_description,
            pdf_link=f"/download/{pdf_filename}"
        )

    return render_template('index.html')


@app.route('/download/<path:filename>')
def download_file(filename):
    # Serve file from current working directory
    return send_from_directory(directory=os.getcwd(), path=filename, as_attachment=True)


if __name__ == "__main__":
    print("✅ Starting Resume Selector Flask App...")
    app.run(debug=True)


# structure

# smart_resume_selector/
# ├── app.py
# ├── .env
# ├── requirements.txt
# ├── templates/
# │   ├── index.html
# │   └── results.html
# ├── resumes/                     Resume uploads
# ├── utils/
# │   ├── resume_reader.py
# │   ├── gemini_ranker.py
# │   └── generate_pdf_report.py