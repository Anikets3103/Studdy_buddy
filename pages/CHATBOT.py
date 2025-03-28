import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-pro-exp")  # Using Gemini Pro model
chat = model.start_chat(history=[])
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom right, #2E0854, #000000);
            color: white;
            text-align: left;
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

st.title("💬 Your Personal AI-Learning Assistant")
st.write("Ask me anything!")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = chat.send_message(user_input)
    ai_reply = response.text  

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.spinner("Generating Response..."):
        with st.chat_message("assistant"):
            st.write(ai_reply)
