import streamlit as st
from streamlit.components.v1 import html
import sys
import os
from dotenv import load_dotenv

load_dotenv()  

API_KEY = os.getenv("GOOGLE_API_KEY")

sys.path.append(os.path.abspath("pages"))


st.set_page_config(page_title="Smart Study Buddy", layout="centered")


st.markdown(
    """
    <style>
         /* Animated Gradient Background */
        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(-45deg, 
                        #0d1117,   /* Dark base */
                    #006400,   /* Dark Green */
                    #000000,   /* Black */
                    #8B0000,   /* Dark Red */
                    #2E0854,   /* Old purple */
                    #8B008B    /* Dark Magenta */
            );
            background-size: 500% 500%;
            animation: gradientShift 20s ease infinite;
            color: white;
            text-align: center;
            height: 100vh;
            overflow: hidden;
        }

         /* ===== Floating Emoji Animation ===== */
        .emoji {
            position: absolute;
            font-size: 28px;
            opacity: 0.85;
            animation: floatEmoji 12s linear infinite;
        }

        @keyframes floatEmoji {
            0% { transform: translateY(110vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            50% { transform: translateY(50vh) rotate(180deg); }
            90% { opacity: 1; }
            100% { transform: translateY(-20vh) rotate(360deg); opacity: 0; }
        }

        /* ===== Buttons ===== */
        .stButton>button {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            color: white;
            font-weight: bold;
            border-radius: 14px;
            padding: 12px 20px;
            font-size: 18px;
            border: none;
            box-shadow: 0px 4px 12px rgba(0, 114, 255, 0.4);
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background: linear-gradient(to right, #00e5ff, #0099ff);
            transform: scale(1.05);
            box-shadow: 0px 6px 16px rgba(0, 200, 255, 0.7);
        }

        /* ===== Titles ===== */
        h1, h2, h3 {
            text-shadow: 0px 0px 12px rgba(0, 200, 255, 0.7);
            font-family: 'Segoe UI', sans-serif;
        }
    </style>

    <!-- Floating Emojis -->
    <div class="floating-emojis">
        """ + "".join([
            f"<div class='emoji' style='left:{i*10+5}%; animation-delay:{i*2}s;'>{e}</div>"
            for i, e in enumerate(["📚","✏️","📝","📖","🖊️","📒","📓","🖍️","📑","📔"])
        ]) + """
    </div>
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
