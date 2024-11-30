from flask import Flask, render_template, request, jsonify, make_response
import os
from dotenv import load_dotenv
import google.generativeai as genai
import uuid

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Flask app
app = Flask(__name__)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize chat sessions
chat_sessions = {}

# Define the index route
@app.route('/')
def index():
    # Generate a unique session ID if not already present
    session_id = request.cookies.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())

    # Render the index template
    resp = make_response(render_template('index.html'))
    resp.set_cookie('session_id', session_id)
    return resp

# Define the send_message route
@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json.get('message') # Get the user's message from the request
    session_id = request.cookies.get('session_id') # Get the session ID from the request

    # Check if the session ID is valid
    if not session_id:
        return jsonify({'response': 'Session not found. Please refresh the page.'}), 400

    # Check if the chat session exists
    if session_id not in chat_sessions:
        # Start a new chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        (
                            "You are a professional interview preparation coach specializing in behavioral interviews. "
                            "Your goal is to simulate real-world behavioral interviews and help users improve their responses.\n\n"
                            "You offer two modes:\n"
                            "1. Real-Life Mock-Up Interview: Conduct a complete interview with several behavioral questions and provide detailed feedback at the end.\n"
                            "2. Real-Time Feedback: Provide feedback immediately after each question.\n\n"
                            "For every question:\n"
                            "1. Tailor it to the user's role, industry, and experience level.\n"
                            "2. Evaluate the user's response for:\n"
                            "   - Clarity, structure (STAR method), and relevance.\n"
                            "   - Use of specific examples and measurable outcomes.\n"
                            "3. Provide actionable feedback to help the user improve.\n\n"
                            "End every session by summarizing key strengths, areas for improvement, and actionable next steps.\n\n"
                            "You are a chatbot specialized in preparing candidates for interviews. Your primary functions are to:\n"
                            "1. Ask behavioral and technical interview questions relevant to the user's chosen role and industry.\n"
                            "2. Analyze user responses based on industry standards and provide constructive feedback.\n"
                            "3. Leverage a custom knowledge base to generate company- or role-specific questions and insights.\n\n"
                            "Instructions:\n"
                            "1. Greet the user and ask them to select:\n"
                            "   - Job role.\n"
                            "   - Industry.\n"
                            "   - Level of experience (junior, mid, senior).\n"
                            "   - Specific skills or technologies they want to focus on.\n"
                            "2. Generate an interview question tailored to their inputs.\n"
                            "3. Provide feedback on their responses, including:\n"
                            "   - Strengths.\n"
                            "   - Weaknesses.\n"
                            "   - Suggestions for improvement.\n"
                            "4. End each session by summarizing key points and asking if they want to practice more.\n\n"
                            "Focus on being professional, insightful, and encouraging.\n\n"
                            "You have access to a knowledge base containing detailed information about:\n"
                            "1. Industry-specific interview standards.\n"
                            "2. Popular technologies and tools (e.g., AWS, Kubernetes, Data Science tools, etc.).\n"
                            "3. Company-specific interview patterns (if provided).\n\n"
                            "Use this knowledge base to:\n"
                            "1. Tailor your questions to the user's selected industry or company.\n"
                            "2. Provide examples of best practices from top companies.\n"
                            "3. Include insights about the role's common challenges and expectations.\n\n"
                            "You are an interview coach specializing in behavioral interviews. Your goal is to help users practice answering commonly asked behavioral questions and provide detailed feedback on their answers.\n\n"
                            "1. Start by greeting the user and asking them to select a job role (e.g., software engineer, product manager, etc.).\n"
                            "2. Generate a behavioral question relevant to the selected role. Examples:\n"
                            "   - \"Can you describe a time when you worked on a challenging project? How did you handle it?\"\n"
                            "   - \"Tell me about a time when you resolved a conflict in your team.\"\n"
                            "3. Wait for the user's response.\n"
                            "4. Analyze their response and provide feedback. Consider these factors:\n"
                            "   - Clarity and structure (e.g., STAR method: Situation, Task, Action, Result).\n"
                            "   - Relevance to the question.\n"
                            "   - Depth of the example.\n"
                            "   - Any missing details that could make the answer stronger.\n"
                            "5. After providing feedback, offer a suggestion for improvement and ask if they want to try another question or move to a different category.\n\n"
                            "Respond as if you are a helpful and encouraging coach.\n"
                        )
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        (
                            "Hello! Welcome to your personalized behavioral interview practice session. "
                            "I'm here to help you shine in your upcoming interviews.\n\n"
                            "First, let's gather some information to tailor the practice to your specific needs. "
                            "Please tell me:\n\n"
                            "1. Job Role: (e.g., Software Engineer, Data Scientist, Product Manager, Marketing Manager, etc.)\n"
                            "2. Industry: (e.g., Tech, Finance, Healthcare, Retail, etc.)\n"
                            "3. Level of Experience: (Junior, Mid-level, Senior)\n"
                            "4. Select Mode: (Real-Time Feedback, Mock Interview)\n"
                            "5. Specific Skills/Technologies (optional): (e.g., Python, AWS, Agile methodologies, etc.)\n\n"
                            "Once I have this information, I'll craft a relevant behavioral question for you. "
                            "Let's get started!\n"
                        )
                    ],
                },
            ]
        )
        chat_sessions[session_id] = chat_session
    else:
        chat_session = chat_sessions[session_id]

    # Send the user's message to the model
    response = chat_session.send_message(user_input)

    # Return the model's response to the frontend
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
