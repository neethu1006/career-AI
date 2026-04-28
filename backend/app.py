def fix_broken_lines(text):
    import re
    # Replace single newlines (not double newlines) with a space
    return re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
import re
def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess


from prompts import (
    resume_analysis_prompt,
    interview_question_prompt,
    interview_feedback_prompt
)
from resume_parser import clean_resume

import os
app = Flask(__name__, static_folder=None)
CORS(app)  




def run_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=120
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"

        # Strip ANSI codes and fix broken lines
        clean = strip_ansi_codes(result.stdout.strip())
        clean = fix_broken_lines(clean)
        return clean

    except Exception as e:
        return f"Exception: {str(e)}"





@app.route("/")
def serve_index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../frontend'), 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    frontend_dir = os.path.join(os.path.dirname(__file__), '../frontend')
    if filename in ['script.js', 'style.css']:
        return send_from_directory(frontend_dir, filename)
    return "Not Found", 404



@app.route("/analyze_resume", methods=["POST"])
def analyze_resume():
    data = request.json
    resume_text = data.get("resume", "")

    if not resume_text:
        return jsonify({"error": "No resume provided"}), 400

    cleaned = clean_resume(resume_text)
    prompt = resume_analysis_prompt(cleaned)

    output = run_ollama(prompt)

    return jsonify({"result": output})



@app.route("/generate_question", methods=["POST"])
def generate_question():
    data = request.json
    role = data.get("role", "")

    if not role:
        return jsonify({"error": "No role provided"}), 400

    prompt = interview_question_prompt(role)
    output = run_ollama(prompt)

    return jsonify({"question": output})



@app.route("/interview", methods=["POST"])
def interview():
    data = request.json
    role = data.get("role", "")
    answer = data.get("answer", "")

    if not role or not answer:
        return jsonify({"error": "Missing role or answer"}), 400

    prompt = interview_feedback_prompt(role, answer)
    output = run_ollama(prompt)

    return jsonify({"result": output})



if __name__ == "__main__":
    app.run(debug=True, port=5000)