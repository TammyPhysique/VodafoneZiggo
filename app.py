from flask import Flask, request, send_file, session, render_template_string
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app and configure session
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session handling
app.config['SESSION_TYPE'] = 'filesystem'  # Store session in filesystem

# Define system prompt
system_prompt = """You are a friendly customer service chatbot for Vodafone and ziggo, respond first in dutch, if they want other language they ask.
    I want you to find the answer on their website: [Vodafone](https://www.vodafone.nl and https://www.ziggo.nl/).
    Try to help the customer solve their problem online without calling and help the customer as much as possible, guide customer in a friendly way, act like a human and not like bot until the problem is solved.
"""

# Function to send a prompt to GPT and return the response
def send_gpt(prompt, conversation_history):
    messages = [{"role": "system", "content": system_prompt}] + conversation_history
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

# Define Flask route
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'conversation' not in session:
        session['conversation'] = []  # Initialize conversation history

    response = None
    if request.method == 'POST':
        question = request.form['question']
        # Get conversation history from session
        conversation_history = session['conversation']
        # Get the chatbot response
        response = send_gpt(question, conversation_history)
        # Update the conversation history and save it in the session
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": response})
        session['conversation'] = conversation_history  # Save updated history

    # Display the conversation with the chatbot
    conversation_html = "<br>".join([f"<b>{msg['role'].capitalize()}:</b> {msg['content']}" for msg in session['conversation']])

    # HTML structure, embedded in Python for simplicity
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vodafone Chatbot</title>
        <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
        <h1>Vodafone Chatbot</h1>
        <form method="POST" action="/">
            <label for="question">Ask the chatbot:</label><br><br>
            <input type="text" id="question" name="question" size="50"><br><br>
            <input type="submit" value="Submit">
        </form>
        <br>
        <h3>Conversation:</h3>
        <div>{conversation_html}</div>
    </body>
    </html>
    """
    
    return render_template_string(html_content)  # Using render_template_string for simplicity

if __name__ == '__main__':
    app.run(debug=True)
