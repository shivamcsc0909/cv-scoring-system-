import streamlit as st
from scorer import score_resume
from logger import log_resume_score

st.title("CV Scoring Agent")

uploaded_file = st.file_uploader("Upload a resume (PDF)", type="pdf")

if uploaded_file:
    resume_path = f"resumes/{uploaded_file.name}"
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.read())
    score = score_resume(resume_path)
    log_resume_score(uploaded_file.name, score)
    st.success(f"Resume Score: {score}")
