import streamlit as st
import fitz  
import google.generativeai as genai
import os
import os
from dotenv import load_dotenv

load_dotenv()  

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  


def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text


def summarize_text(text):
    response = model.generate_content(f"Summarize this text:\n\n{text}")
    return response.text

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
    """,
    unsafe_allow_html=True
)

st.title("📄 AI PDF Summarizer")
st.write("Upload a PDF, and I'll summarize it for you!")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        if pdf_text not in st.session_state:
            st.session_state["text"] = pdf_text

    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(pdf_text)
            st.subheader("📌 Summary:")
            st.write(summary)



