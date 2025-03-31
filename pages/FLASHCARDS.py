import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv

load_dotenv()  

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-pro-exp") 
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

st.title("Revise with Flashcards 📚")

def generate_flashcards(text):
    prompt = f"Generate exactly 5 flashcards from the following text in Q&A format:\n\n{text}\n\nFormat each flashcard as:\nQ: <Question>\nA: <Answer>"
    response = model.generate_content(prompt)
    
    # Extract Q&A pairs
    flashcards = response.text.strip().split("\n")

    structured_flashcards = []
    question, answer = None, None
    for line in flashcards:
        if line.startswith("Q:"):
            question = line[3:].strip()
        elif line.startswith("A:"):
            answer = line[3:].strip()
            if question and answer:
                structured_flashcards.append((question, answer))
                question, answer = None, None  # Reset for next Q&A pair
    while len(structured_flashcards) < 5:
        structured_flashcards.append(("Placeholder Question", "Placeholder Answer"))

    return structured_flashcards[:5] 

if st.button("Generate Flashcards"):
    if "text" in st.session_state:
        with st.spinner("Generating flashcards..."):
            flashcards = generate_flashcards(st.session_state["text"])
    
            st.subheader("📚 Flashcards (Hover to Flip!):")
    
            # Updated CSS for vertical layout, padding, and hover flip effect
            flip_card_html = """
            <style>
            .pentagon-container {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                grid-template-rows: repeat(2, 1fr);
                justify-items: center;
                align-items: center;
                width: 100%;
                max-width: 600px;
                margin: auto;
                gap: 20px;
                position: relative;
            }
            .flip-card {
                background-color: transparent;
                width: 200px;
                height: 120px;
                perspective: 1000px;
            }
            .flip-card-inner {
                position: relative;
                width: 100%;
                height: 100%;
                text-align: center;
                transition: transform 0.6s;
                transform-style: preserve-3d;
            }
            .flip-card:hover .flip-card-inner {
                transform: rotateY(180deg);
            }
            .flip-card-front, .flip-card-back {
                position: absolute;
                width: 100%;
                height: 100%;
                backface-visibility: hidden;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 10px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
                font-size: 16px;
                text-align: center;
                font-weight: bold;
            }
            .flip-card-front {
                background: #27004f;
                color: white;
            }
            .flip-card-back {
                background: white;
                color: black;
                transform: rotateY(180deg);
                border: 2px solid #007bff;
            }
            .card-1 { grid-column: 2; grid-row: 1; }
            .card-2 { grid-column: 1; grid-row: 2; }
            .card-3 { grid-column: 3; grid-row: 2; }
            .card-4 { grid-column: 1; grid-row: 3; }
            .card-5 { grid-column: 3; grid-row: 3; }
            </style>
    
            <div class="pentagon-container">
            """
    
            for i, (question, answer) in enumerate(flashcards):
                flip_card_html += f"""
                <div class="flip-card card-{i+1}">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <p>❓ {question}</p>
                        </div>
                        <div class="flip-card-back">
                            <p>✅ {answer}</p>
                        </div>
                    </div>
                </div>
                """
    
            flip_card_html += "</div>"
    
            # Render using st.components.v1.html()
            components.html(flip_card_html, height=500)
    else:
        st.warning("Upload file first")
