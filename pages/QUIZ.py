import streamlit as st
import random
import google.generativeai as genai
from typing import List, Dict, Optional
import os

# Configure Gemini API (assumes API key is set in environment variables)
genai.configure(api_key="AIzaSyDdHp8h1aHJPbjQ44aSYY_LUibeIcUjJ24")
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Data structure for a single MCQ
class MCQ:
    def __init__(self, question: str, options: List[str], correct_answer: str):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

def generate_mcqs_from_text(text: str, num_questions: int) -> List[MCQ]:
    """Generate multiple MCQs at once using Gemini API"""
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
                question = line.split(":")[1].strip()
                options = []
                correct_answer = ""
            elif line.startswith(("A)", "B)", "C)", "D)")):
                options.append(line[3:].strip())
            elif line.startswith("Answer:"):
                correct_letter = line.split(":")[1].strip()
                correct_answer = options[ord(correct_letter) - ord('A')]

        if question and len(options) == 4 and correct_answer:
            mcqs.append(MCQ(question, options, correct_answer))

        return mcqs[:num_questions]  # Return only the requested number

    except Exception as e:
        st.error(f"Error generating MCQs: {str(e)}")
        return []

def generate_quiz(text: str, num_questions: int) -> List[MCQ]:
    """Generate specified number of unique MCQs"""
    quiz = []
    attempts = 0
    max_attempts = num_questions * 2  # Prevent infinite loop
    
    while len(quiz) < num_questions and attempts < max_attempts:
        mcq = generate_mcqs_from_text(text)
        if mcq and mcq.question not in [q.question for q in quiz]:
            # Shuffle options
            correct_idx = mcq.options.index(mcq.correct_answer)
            random.shuffle(mcq.options)
            mcq.correct_answer = mcq.options[correct_idx]
            quiz.append(mcq)
        attempts += 1
    
    return quiz[:num_questions]

def initialize_session_state():
    """Initialize necessary session state variables"""
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

    st.title("Multiple Choice Quiz Generator")
    
    # Initialize session state
    initialize_session_state()
    
    # Check if text is available
    if "text" not in st.session_state or not st.session_state["text"]:
        st.warning("Please upload a PDF first to generate questions!")
        return
    
    # Number of questions selector
    num_questions = st.slider("How many questions would you like?", 
                            min_value=1, 
                            max_value=10, 
                            value=5)
    
    # Generate quiz button
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz questions..."):
            st.session_state.quiz = generate_quiz(st.session_state["text"], num_questions)
            st.session_state.current_question = 0
            st.session_state.submitted = False
            st.session_state.user_answer = None
    
    # Display quiz if generated
    if st.session_state.quiz:
        total_questions = len(st.session_state.quiz)
        current_idx = st.session_state.current_question
        
        if current_idx < total_questions:
            mcq = st.session_state.quiz[current_idx]
            
            # Display question
            st.subheader(f"Question {current_idx + 1} of {total_questions}")
            st.write(mcq.question)
            
            # Display options
            options = mcq.options
            user_answer = st.radio("Select your answer:", 
                                 options, 
                                 key=f"q_{current_idx}",
                                 disabled=st.session_state.submitted)
            
            # Submit button
            if not st.session_state.submitted:
                if st.button("Submit Answer"):
                    st.session_state.user_answer = user_answer
                    st.session_state.submitted = True
                    st.rerun()
            
            # Show result if submitted
            if st.session_state.submitted:
                is_correct = st.session_state.user_answer == mcq.correct_answer
                st.write(f"Your answer: {st.session_state.user_answer}")
                st.write(f"Correct answer: {mcq.correct_answer}")
                st.write("✅ Correct!" if is_correct else "❌ Incorrect!")
                
                # Next question button
                if st.button("Next Question"):
                    st.session_state.current_question += 1
                    st.session_state.submitted = False
                    st.session_state.user_answer = None
                    st.rerun()
        
        else:
            st.success("Quiz completed! Click 'Generate Quiz' to start a new one.")
    
    # Error handling for insufficient questions
    if st.session_state.quiz and len(st.session_state.quiz) < num_questions:
        st.warning(f"Could only generate {len(st.session_state.quiz)} out of {num_questions} questions.")

if __name__ == "__main__":
    main()