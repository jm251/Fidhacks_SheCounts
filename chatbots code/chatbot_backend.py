from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import random
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
CORS(app)

# Configure AI services
genai.configure(api_key="YOUR_API_KEY_HERE")  # Replace with your actual API key like this AIzaSyCC8lv6ylyiq2f4csBH8LX1bktSaoDBqyMP
model = genai.GenerativeModel('gemini-pro')

# Initialize sentence transformer
sentence_model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Pinecone configuration
pc = Pinecone(api_key='YOUR_PINECONE_API_KEY_HERE')  # Replace with your actual API key like this pcsk_f78ui_DiRV152wxnikF4juHxcJsNEAtBZNNeuQqhGSofUKgm76W7NmdKBhXCg5y6U1kJrP
index_name = "fidhacks"

try:
    index = pc.Index(index_name)
except:
    print("Warning: Could not connect to Pinecone index. Resource lookup will be disabled.")
    index = None

safety_instruction = "Please ensure that the content you generate is safe, appropriate, and free from explicit or harmful language."

class ChatbotAPI:
    def __init__(self):
        self.chat = model.start_chat(history=[])
        self.current_question = ""
        self.correct_answer = ""
    
    def generate_question(self, topic="financial literacy"):
        """Generate a random question related to the specified topic"""
        question_instruction = f"Generate a random question related to {topic}. Respond with 'Question: [generated question]'."
        question = ""
        
        try:
            question_response = self.chat.send_message(safety_instruction + " " + question_instruction)
            if "Question:" in question_response.text:
                question = question_response.text.split("Question:")[-1].strip()
            else:
                question = question_response.text.strip()
        except StopCandidateException as e:
            question = "What is the recommended amount for an emergency fund?"
        except Exception as e:
            question = "What factors should you consider when choosing a credit card?"
        
        self.current_question = question
        return question
    
    def generate_answer(self):
        """Generate the correct answer for the current question"""
        if not self.current_question:
            return "No question available."
        
        answer_instruction = f"Provide the correct answer to the following question: {self.current_question}. Respond with 'Answer: [correct answer]'."
        correct_answer = ""
        
        try:
            answer_response = self.chat.send_message(safety_instruction + " " + answer_instruction)
            if "Answer:" in answer_response.text:
                correct_answer = answer_response.text.split("Answer:")[-1].strip()
            else:
                correct_answer = answer_response.text.strip()
        except StopCandidateException as e:
            correct_answer = "Please refer to financial literacy resources for the correct answer."
        except Exception as e:
            correct_answer = "Unable to generate answer at this time."
        
        self.correct_answer = correct_answer
        return correct_answer
    
    def evaluate_answer(self, user_answer):
        """Evaluate the user's answer against the correct answer"""
        if not self.current_question or not self.correct_answer:
            return {"is_correct": False, "message": "No question or answer available."}
        
        evaluation_instruction = f"""
        Question: {self.current_question}
        User's Answer: {user_answer}
        Correct Answer: {self.correct_answer}
        
        Based on the provided correct answer, is the user's answer correct? 
        Respond with 'Evaluation: Correct' if the user's answer is correct, 
        or 'Evaluation: Incorrect' if it is incorrect.
        """
        
        try:
            evaluation_response = self.chat.send_message(safety_instruction + " " + evaluation_instruction)
            is_correct = "Correct" in evaluation_response.text
            
            result = {
                "is_correct": is_correct,
                "message": evaluation_response.text,
                "correct_answer": self.correct_answer
            }
            
            if not is_correct and index:
                # Get relevant resource
                resource = self.get_relevant_resource(self.correct_answer)
                if resource:
                    result["resource"] = resource
            
            return result
            
        except Exception as e:
            return {
                "is_correct": False,
                "message": f"Error evaluating answer: {str(e)}",
                "correct_answer": self.correct_answer
            }
    
    def get_relevant_resource(self, query_text):
        """Get relevant resource from Pinecone based on query"""
        if not index:
            return None
        
        try:
            temp_emb = sentence_model.encode(query_text).tolist()
            query_results = index.query(
                namespace="auto_loan_resources",
                vector=temp_emb,
                top_k=1,
                include_metadata=True
            )
            
            if query_results.matches:
                top_match_metadata = query_results.matches[0].metadata
                return {
                    "title": top_match_metadata.get('title', 'Financial Resource'),
                    "link": top_match_metadata.get('link', '#'),
                    "description": top_match_metadata.get('description', '')
                }
        except Exception as e:
            print(f"Error getting resource: {e}")
        
        return None
    
    def handle_general_question(self, question):
        """Handle general financial literacy questions"""
        instruction = f"Answer this financial literacy question: {question}. Provide a helpful, educational response."
        
        try:
            response = self.chat.send_message(safety_instruction + " " + instruction)
            return response.text
        except Exception as e:
            return "I apologize, but I'm having trouble answering that question right now. Please try again."

# Initialize chatbot
chatbot = ChatbotAPI()

@app.route('/')
def index():
    return render_template('chatbot_frontend.html')

@app.route('/api/generate_question', methods=['POST'])
def api_generate_question():
    try:
        data = request.get_json()
        topic = data.get('topic', 'financial literacy')
        question = chatbot.generate_question(topic)
        
        return jsonify({
            'success': True,
            'question': question
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/submit_answer', methods=['POST'])
def api_submit_answer():
    try:
        data = request.get_json()
        user_answer = data.get('answer', '')
        
        # First generate the correct answer
        chatbot.generate_answer()
        
        # Then evaluate the user's answer
        evaluation = chatbot.evaluate_answer(user_answer)
        
        return jsonify({
            'success': True,
            'evaluation': evaluation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/ask_question', methods=['POST'])
def api_ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        response = chatbot.handle_general_question(question)
        
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/reset_chat', methods=['POST'])
def api_reset_chat():
    try:
        global chatbot
        chatbot = ChatbotAPI()
        
        return jsonify({
            'success': True,
            'message': 'Chat reset successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
