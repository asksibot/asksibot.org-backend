from flask import render_template, request, jsonify
# Ensure the import path matches the location of your create_app function
from config import create_app
from openai import OpenAI

client = OpenAI(api_key=app.config['OPENAI_API_KEY'])

# Initialize Flask application
app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    # Extract the message from the POST request
    data = request.get_json()
    user_message = data['message']

    # Ensure you have your OpenAI API key set in your Flask app's config

    try:
        # Make a call to OpenAI API with the user's message
        response = client.chat.completions.create(model=app.config['OPENAI_ENGINE'],  # Use the engine set in config
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ])
        # Extract the text of the response
        bot_response = response.choices[0].message.content.strip() if response.choices else "I'm not sure how to respond to that."
    except Exception as e:
        # Handle exceptions, such as errors in communicating with OpenAI API
        print(f"Error while calling OpenAI API: {e}")
        bot_response = 'Sorry, I am having trouble understanding that.'

    return jsonify({'bot_response': bot_response})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
