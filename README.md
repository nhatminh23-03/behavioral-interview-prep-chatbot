# Behavioral Interview Prep Chatbot

This project is a chatbot designed to help users prepare for behavioral interviews. It uses **Flask** for the backend and the **Google Gemini API** to generate and analyze responses, providing real-time or mock interview feedback tailored to the user's role, industry, and experience level.

## Features

- **Real-Time Feedback Mode**: Provides immediate feedback after each response.
- **Mock Interview Mode**: The user can either do a full interview session or summarize feedback at the end.
- **Role-Specific Questions**: Generates questions tailored to the user's job role, industry, and experience.
- **Constructive Feedback**: Uses the STAR method (Situation, Task, Action, Result) to evaluate responses.

## Installation

### Prerequisites
- Python 3.9 or higher
- A valid Google Gemini API key
- Visual Studio Code (Recommended)

### Installation Steps

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/nhatminh23-03/behavioral-interview-prep-chatbot.git
2. Navigate to the project directory:
   ```bash
   cd behavioral-interview-prep-chatbot
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate # For window: venv\Scripts\activate
5. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
6. Create an .env file to store your API key: In the project root, create a file named .env and add the following line:
   ```bash
   GEMINI_API_KEY=your_api_key_here
7. Open the project in VS Code (recommend):
   ```bash
   code .
8. Run the chatbot:
   ```bash
   python app.py
9. Access the chatbot in your browser:
   After running the command above, you will see a message in the terminal similar to this:
   For example:
   ```bash
   Running on http://127.0.0.1:5000/
Open your browser and navigate to the URL to interact with the chatbot.




   
   
