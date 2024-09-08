import os
from flask import Flask, request, send_file
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY='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'


# Initialize Flask app
app = Flask(__name__)

# Define system prompt
system_prompt = (
    """You are a friendly customer service chatbot for Vodafone/ziggo.
    Try to assist the customer as much as possible. Greet the customer and ask how you can help."""
)

# Function to send a prompt to GPT
def send_gpt(prompt):
    try:
        # Use OpenAI API to create chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        response_message = response['choices'][0]['message']['content']
        return response_message
    except Exception as e:
        return str(e)

# Define Flask route
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        question = request.form['question']
        response = send_gpt(question)
        return f"<h1>Chatbot Response: {response}</h1>"
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
