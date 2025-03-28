import streamlit as st
import fitz  
import google.generativeai as genai
import os
import os
from dotenv import load_dotenv

load_dotenv()  

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-pro-exp")  


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



