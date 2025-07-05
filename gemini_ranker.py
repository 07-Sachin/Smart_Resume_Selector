import google.generativeai as genai
import os

# 🔐 Load your Gemini API key
genai.configure(api_key=os.getenv("GRMINI API KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')  # Use the appropriate model version

import re

def extract_score(text):
    text = text.lower()
    match_10 = re.search(r'(\d+(\.\d+)?)\s*/\s*10', text)
    match_100 = re.search(r'(\d+(\.\d+)?)\s*/\s*100', text)
    match_1000 = re.search(r'(\d+(\.\d+)?)\s*/\s*1000', text)
    match_out_of = re.search(r'(\d+(\.\d+)?)\s*out\s*of\s*(10|100|1000)', text)
    match_percent = re.search(r'(\d+(\.\d+)?)\s*%', text)

    if match_10:
        return round(float(match_10.group(1)), 1)
    elif match_100:
        return round(float(match_100.group(1)) / 10, 1)
    elif match_1000:
        return round(float(match_1000.group(1)) / 100, 1)
    elif match_out_of:
        score = float(match_out_of.group(1))
        base = int(match_out_of.group(3))
        return round(score / base * 10, 1)
    elif match_percent:
        return round(float(match_percent.group(1)) / 10, 1)
    return 0


def rank_resumes_with_gemini(job_desc, resumes):
    ranked_results = []

    for resume in resumes:
        prompt = f"""You are a smart recruiter assistant.

Given this job description:
\"\"\"{job_desc}\"\"\"

Evaluate the following resume:
\"\"\"{resume['content']}\"\"\"

How well does it match the job description? Give a score out of 10 and explain briefly.
"""

        response = model.generate_content(prompt)
        content = response.text

        # Parse out score (rough method)
        score_line = [line for line in content.split('\n') if 'score' in line.lower()]
        score = int(''.join(filter(str.isdigit, score_line[0]))) if score_line else 0
        score = extract_score(content)


        ranked_results.append({
            'filename': resume['filename'],
            'score': score,
            'snippet': resume['content'][:400] + '...',
            'full_content': resume['content']  # Add this
        })

    return sorted(ranked_results, key=lambda x: x['score'], reverse=True)