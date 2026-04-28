
let resumeData = "";
let interviewData = { role: "", answer: "", question: "", review: "" };

window.onload = function() {
    const headline = document.getElementById('headline');
    setTimeout(() => {
        headline.classList.add('headline-shrink');
        setTimeout(() => {
            document.getElementById('headline-container').style.height = '80px';
            // Keep headline visible at the top middle
            document.getElementById('main-content').style.display = 'flex';
            renderSideBySide();
        }, 1600);
    }, 2200);
};

function renderSideBySide() {
    document.getElementById('main-content').className = 'side-by-side';
    document.getElementById('main-content').innerHTML = `
        <div class="resume-analyzer-box" style="min-width:340px;max-width:520px;width:100%;">
            <h2>Resume Analyzer</h2>
            <textarea id="resume" placeholder="Paste your resume...">${resumeData}</textarea>
            <button class="main-btn" onclick="analyzeResume()">Analyze</button>
            <div id="resume-output">${window.lastResumeOutput || ''}</div>
        </div>
        <div class="interview-coach-box" style="min-width:340px;max-width:520px;width:100%;">
            <h2>Interview Coach</h2>
            <input id="role" placeholder="Enter role (e.g. Software Engineer)" value="${interviewData.role}">
            <button class="main-btn" onclick="getQuestion()">Get Question</button>
            <div id="question">${interviewData.question || ''}</div>
            <textarea id="answer" placeholder="Type your answer...">${interviewData.answer}</textarea>
            <button class="main-btn" onclick="submitAnswer()">Submit Answer</button>
            <div id="interview-output">${interviewData.review || ''}</div>
        </div>
    `;
    document.getElementById('resume').addEventListener('input', function(e) {
        resumeData = e.target.value;
    });
    document.getElementById('role').addEventListener('input', function(e) {
        interviewData.role = e.target.value;
    });
    document.getElementById('answer').addEventListener('input', function(e) {
        interviewData.answer = e.target.value;
    });
}

async function analyzeResume() {
    const resume = document.getElementById("resume").value;
    resumeData = resume;
    const btn = document.querySelectorAll('.main-btn')[0];
    btn.disabled = true;
    btn.innerText = 'Analyzing...';
    const res = await fetch("http://127.0.0.1:5000/analyze_resume", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({resume})
    });
    const data = await res.json();
    window.lastResumeOutput = `<pre>${data.result}</pre>`;
    document.getElementById("resume-output").innerHTML = window.lastResumeOutput;
    btn.disabled = false;
    btn.innerText = 'Analyze';
}

async function getQuestion() {
    const role = document.getElementById("role").value;
    const btn = document.querySelectorAll('.main-btn')[1];
    btn.disabled = true;
    btn.innerText = 'Loading...';
    const res = await fetch("http://127.0.0.1:5000/generate_question", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({role})
    });
    const data = await res.json();
    document.getElementById("question").innerText = data.question;
    btn.disabled = false;
    btn.innerText = 'Get Question';
}

async function submitAnswer() {
    const role = document.getElementById("role").value;
    const answer = document.getElementById("answer").value;
    const btn = document.querySelectorAll('.main-btn')[2];
    btn.disabled = true;
    btn.innerText = 'Reviewing...';
    const res = await fetch("http://127.0.0.1:5000/interview", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({role, answer})
    });
    const data = await res.json();
    document.getElementById("interview-output").innerHTML = `<pre>${data.result}</pre>`;
    btn.disabled = false;
	btn.innerText = 'Submit Answer';
}
