import streamlit as st
import os
import random
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException
from pinecone import Pinecone, ServerlessSpec
import transformers
from sentence_transformers import SentenceTransformer

genai.configure()
genai.configure(api_key="API key")
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Model
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Pinecone
pc = Pinecone(api_key='API Key')
index_name = "fidhacks"
index = pc.Index(index_name)

st.title("(Topic) Chatbot")

if 'question' not in st.session_state:
    st.session_state.question = ""
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = ""
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = ""

safety_instruction = "Please ensure that the content you generate is safe, appropriate, and free from explicit or harmful language."

def generate_question():
    question_instruction = "Generate a random question related to (topic). Respond with 'Question: [generated question]'."
    question = ""
    while True:
        try:
            question_response = chat.send_message(safety_instruction + " " + question_instruction)
            if "Question:" in question_response.text:
                question = question_response.text.split("Question:")[-1].strip()
                break
        except StopCandidateException as e:
            st.warning("Gemini: I apologize, but the generated question contained content that triggered a safety rating.")
            st.warning("Generating a new question...")
            continue
    st.session_state.question = question

def generate_answer():
    answer_instruction = "Provide the correct answer to the following question: " + st.session_state.question + ". Respond with 'Answer: [correct answer]'."
    correct_answer = ""
    while True:
        try:
            answer_response = chat.send_message(safety_instruction + " " + answer_instruction)
            if "Answer:" in answer_response.text:
                correct_answer = answer_response.text.split("Answer:")[-1].strip()
                break
        except StopCandidateException as e:
            st.warning("Gemini: I apologize, but the generated answer contained content that triggered a safety rating.")
            st.warning("Generating a new answer...")
            continue
    st.session_state.correct_answer = correct_answer

def evaluate_answer():
    evaluation_instruction = f"Question: {st.session_state.question}\nUser's Answer: {st.session_state.user_answer}\nCorrect Answer: {st.session_state.correct_answer}\n\nBased on the provided correct answer, is the user's answer correct? Respond with 'Evaluation: Correct' if the user's answer is correct, or 'Evaluation: Incorrect' if it is incorrect."
    evaluation_response = chat.send_message(safety_instruction + " " + evaluation_instruction)
    st.session_state.evaluation = evaluation_response.text

    if "Correct" in evaluation_response.text:
        st.success("Correct! Click the next button to continue.")
    else:
        st.error(f"Incorrect. The correct answer is: {st.session_state.correct_answer}")
        temp_emb = model.encode(st.session_state.correct_answer).tolist()
        query_results = index.query(
            namespace="auto_loan_resources",
            vector=temp_emb,
            top_k=1,
            include_metadata=True
        )
        if query_results.matches:
            top_match_metadata = query_results.matches[0].metadata
            st.info("Here's a helpful resource related to the question:")
            st.write(f"Title: {top_match_metadata.get('title')}")
            st.write(f"Link: {top_match_metadata.get('link')}")
        else:
            st.warning("Sorry, I couldn't find a relevant resource in the database.")

if st.button("Generate Question"):
    generate_question()

st.write(st.session_state.question)

st.text_input("Your Answer", key="user_answer")

if st.button("Submit Answer"):
    generate_answer()
    evaluate_answer()
