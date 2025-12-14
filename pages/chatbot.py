import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")  # Using Gemini Pro model
chat = model.start_chat(history=[])
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
