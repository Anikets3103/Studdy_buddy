import streamlit as st
import random
import google.generativeai as genai
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# MCQ Data Structure
class MCQ:
    def __init__(self, question: str, options: List[str], correct_answer: str):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

# Generate MCQs

def generate_mcqs_from_text(text: str, num_questions: int) -> List[MCQ]:
    """Generate multiple MCQs using Gemini API."""
    try:
        prompt = f"""
        Given the following text:
        {text[:2000]}

        Generate {num_questions} multiple-choice questions. 
        Each question must have:
        - A unique question based on the text
        - 4 answer options (A, B, C, D)
        - One correct answer, clearly labeled

        Format:
        Q1: [Question]
        A) [Option 1]
        B) [Option 2]
        C) [Option 3]
        D) [Option 4]
        Answer: [A/B/C/D]
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        mcqs = []
        lines = response_text.split("\n")
        question, options, correct_answer = "", [], ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("Q"):  # New Question
                if question and len(options) == 4 and correct_answer:
                    mcqs.append(MCQ(question, options, correct_answer))
                question = line.split(":", 1)[1].strip()
                options = []
                correct_answer = ""
            elif line.startswith(("A)", "B)", "C)", "D)")):
                options.append(line[3:].strip())
            elif line.startswith("Answer:") and options:
                correct_letter = line.split(":")[1].strip()
                if correct_letter in "ABCD":
                    correct_answer = options["ABCD".index(correct_letter)]
        
        if question and len(options) == 4 and correct_answer:
            mcqs.append(MCQ(question, options, correct_answer))
        
        return mcqs[:num_questions]
    except Exception as e:
        st.error(f"Error generating MCQs: {str(e)}")
        return []

# Generate Quiz

def generate_quiz(text: str, num_questions: int) -> List[MCQ]:
    quiz = generate_mcqs_from_text(text, num_questions)
    for mcq in quiz:
        random.shuffle(mcq.options)
    return quiz

# Initialize session state

def initialize_session_state():
    if "quiz" not in st.session_state:
        st.session_state.quiz = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = None
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

def main():
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
    st.title("Multiple Choice Quiz Generator")
    initialize_session_state()
    
    if "text" not in st.session_state or not st.session_state.text:
        st.warning("Please upload a PDF first to generate questions!")
        return
    
    num_questions = st.slider("How many questions would you like?", 1, 10, 5)
    
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz questions..."):
            st.session_state.quiz = generate_quiz(st.session_state.text, num_questions)
            st.session_state.current_question = 0
            st.session_state.submitted = False
            st.session_state.user_answer = None
            st.session_state.score = 0
    
    if st.session_state.quiz:
        total_questions = len(st.session_state.quiz)
        current_idx = st.session_state.current_question
        
        if current_idx < total_questions:
            mcq = st.session_state.quiz[current_idx]
            st.subheader(f"Question {current_idx + 1} of {total_questions}")
            st.write(mcq.question)
            
            user_answer = st.radio("Select your answer:", mcq.options, key=f"q_{current_idx}", disabled=st.session_state.submitted)
            
            if not st.session_state.submitted and st.button("Submit Answer"):
                st.session_state.user_answer = user_answer
                st.session_state.submitted = True
                st.rerun()
            
            if st.session_state.submitted:
                is_correct = st.session_state.user_answer == mcq.correct_answer
                st.write(f"Your answer: {st.session_state.user_answer}")
                st.write(f"Correct answer: {mcq.correct_answer}")
                st.write("✅ Correct!" if is_correct else "❌ Incorrect!")
                if is_correct:
                    st.session_state.score+=1
                
                if st.button("Next Question"):
                    st.session_state.current_question += 1
                    st.session_state.submitted = False
                    st.session_state.user_answer = None
                    st.rerun()
        else:
            st.success("Quiz completed! Click 'Generate Quiz' to start a new one.")
            st.subheader(f"Score : {st.session_state.score//2}/{num_questions}")

if __name__ == "__main__":
    main()
