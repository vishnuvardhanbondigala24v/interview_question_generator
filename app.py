
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# ✅ Set page config FIRST
st.set_page_config(page_title="AI Interview Studio", page_icon="", layout="wide")

# ✅ Centered professional title
st.markdown("""
<div style='text-align: center; padding-top: 20px;'>
    <h1 style='font-size: 48px; color: #2c3e50;'> AI Interview Questions Practice</h1>
    <p style='font-size: 20px; color: #7f8c8d;'>Your personalized AI-powered interview preparation assistant</p>
</div>
""", unsafe_allow_html=True)

# ✅ Then continue with the rest of your app
from question_generator import generate_questions
from resume_parser import extract_resume_text
from skills_extractor import extract_skills
from answer_evaluator import evaluate_answer

# ----------------- PREMIUM STYLING -----------------
st.markdown("""
<style>
body {
    background-color: #eef2f7;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #2c3e50;
}
.question-block {
    background: linear-gradient(to right, #ffffff, #e6ecf5);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}
.question-title {
    font-size: 20px;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 12px;
}
textarea {
    width: 100%;
    font-size: 16px;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #ccc;
    resize: vertical;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
}
.mic-button {
    position: absolute;
    right: 16px;
    top: 40px;
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #3498db;
}
.evaluate-button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 8px;
    margin-top: 10px;
    cursor: pointer;
}
.evaluate-button:hover {
    background-color: #2980b9;
}
</style>
<script>
function startDictation(targetId) {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Speech recognition only works in Chrome.');
        return;
    }
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        document.getElementById(targetId).value = event.results[0][0].transcript;
    };
}
</script>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
st.sidebar.title("⚙️ Controls")
job_role = st.sidebar.text_input("Job Role (e.g., Data Scientist)")
difficulty = st.sidebar.radio("Difficulty", ["easy", "medium", "hard"], index=1)
categories = st.sidebar.multiselect("Categories", ["technical", "behavioral", "situational", "hr"], default=["technical", "behavioral"])
num_questions = st.sidebar.slider("Number of Questions", min_value=1, max_value=30, value=5)

job_description = st.sidebar.text_area("Paste Job Description")

context_text = job_description.strip()
skills_list = extract_skills(context_text) if context_text else []

if st.sidebar.button("🚀 Generate Questions"):
    if job_role:
        questions = generate_questions(
            job_role,
            skills=skills_list if skills_list else None,
            difficulty=difficulty,
            categories=categories,
            num_questions=num_questions
        )
        st.session_state["questions"] = questions
        st.session_state["skills"] = skills_list
        st.success("✅ Questions generated!")
    else:
        st.warning("⚠️ Please enter a job role.")

# ----------------- MAIN CONTENT -----------------
if "questions" in st.session_state:
    st.subheader("📋 Generated Questions & Your Answers")
    for i, q in enumerate(st.session_state["questions"], 1):
        st.markdown(f"""<div class="question-block">
            <div class="question-title">Q{i}: {q}</div>
            <div style="position: relative;">
                <textarea id="answer_{i}" rows="4" placeholder="Type or speak your answer..."></textarea>
                <button class="mic-button" onclick="startDictation('answer_{i}')">🎙️</button>
            </div>
        </div>""", unsafe_allow_html=True)

        user_answer = st.text_area("", key=f"answer_{i}")

        if st.button(f"Evaluate Answer {i}"):
            result = evaluate_answer(q, user_answer)
            st.write(f"📊 Score: {result['score']} / 100")
            st.write(f"✅ Correct: {result['correct']}")
            st.info(f"💡 Feedback: {result['feedback']}")

    st.download_button("⬇️ Download as TXT", "\n".join(st.session_state["questions"]), "questions.txt")
    st.download_button("⬇️ Download as CSV", pd.DataFrame(st.session_state["questions"], columns=["Question"]).to_csv(index=False), "questions.csv")

    st.subheader("📊 Question Breakdown")
    df = pd.DataFrame({"Category": categories, "Count": [len(st.session_state["questions"]) // len(categories)] * len(categories)})
    fig = px.bar(df, x="Category", y="Count", color="Category", title="Questions by Category")
    st.plotly_chart(fig, use_container_width=True)

    if "skills" in st.session_state and st.session_state["skills"]:
        st.subheader("🛠️ Extracted Skills")
        st.write(", ".join(st.session_state["skills"]))
        df_skills = pd.DataFrame({"Skill": st.session_state["skills"], "Count": [1] * len(st.session_state["skills"])})
        fig2 = px.bar(df_skills, x="Skill", y="Count", title="Skills Extracted from Job Description", color="Skill")
        st.plotly_chart(fig2, use_container_width=True)