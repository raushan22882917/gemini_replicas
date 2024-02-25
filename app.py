from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Configure the generative AI
genai.configure(api_key="AIzaSyBTc042cwNJZNyRUQcrUtoHr-LAzLcEA6o")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": [user_input]
        },
        {
            "role": "model",
            "parts": [""]  # Dummy message
        },
    ])

    # Send user input and get the model's response
    convo.send_message(user_input)

    # Return the model's response
    return jsonify({'response': convo.last.text})

if __name__ == "__main__":
    app.run(port=5000)
