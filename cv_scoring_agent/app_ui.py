import streamlit as st
from src.app.parser import parse_resume
from src.app.scorer import score_resume

st.title("Resume Scoring Agent")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
if uploaded_file is not None:
    text = parse_resume(uploaded_file)
    score = score_resume(text)
    st.success(f"Score: {score}/100")
