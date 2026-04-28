

def resume_analysis_prompt(resume_text):
    return f"""
You are a professional ATS (Applicant Tracking System) and career coach.

Analyze the following resume.

Return STRICTLY in this format, using ONLY bullet points (no sentences or paragraphs) for each section:

Score: <number out of 10>

Strengths:
- bullet point 1
- bullet point 2

Weaknesses:
- bullet point 1
- bullet point 2

Improvements:
- bullet point 1
- bullet point 2

IMPORTANT: Do NOT write any sentences or paragraphs. Each item must be a short, clear bullet point.

Resume:
{resume_text}
"""


def interview_question_prompt(role):
    return f"""
You are a professional interviewer.

Generate ONE interview question for a {role} role.

Only output the question.
"""


def interview_feedback_prompt(role, answer):
    return f"""
You are interviewing a candidate for {role}.

Evaluate their answer.

Return STRICTLY in this format, using ONLY bullet points (no sentences or paragraphs) for the Feedback section:

Score: <number out of 10>

Feedback:
- bullet point 1
- bullet point 2

Better Answer:
<improved version>

IMPORTANT: Do NOT write any sentences or paragraphs in the Feedback section. Each item must be a short, clear bullet point.

Candidate Answer:
{answer}
"""