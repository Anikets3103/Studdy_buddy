import streamlit as st
from streamlit.components.v1 import html
import sys
import os

# Add 'my_project' folder to Python's module search path
sys.path.append(os.path.abspath("pages"))

# Set page config
st.set_page_config(page_title="Smart Study Buddy", layout="centered")

# Custom CSS for full-page gradient purple and black background
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom right, #2E0854, #000000);
            color: white;
            text-align: center;
            height: 100vh;
        }
        .stButton>button {
            background: linear-gradient(to right, #4B0082, #2E0854); /* Matching purple gradient */
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px;
            font-size: 18px;
            transition: 0.3s;
            margin-bottom: 4px;
            border: none;
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #6A0DAD, #4B0082);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🚀 Smart Study Buddy")

# Buttons
col1, col2= st.columns(2)

with col1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    if st.button("📄 PDF Summarizer"):
        st.switch_page("pages/pdf_summarizer.py")
    st.write("")
    st.write("")
    if st.button("💬 AI Chatbot"):
        st.switch_page("pages/chatbot.py")

with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    if st.button("📚 Generate Flashcards"):
        st.switch_page("pages/flashcards.py")
    st.write("   ")
    st.write("")
    if st.button("📝 Quizzes"):
        st.switch_page("pages/quiz.py")
