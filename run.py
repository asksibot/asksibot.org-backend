from flask import render_template, request, jsonify
from config import create_app
import openai

# Initialize Flask application and Flask-Mail (if used)
app, mail = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    # Extract the message from the POST request
    data = request.get_json()
    user_message = data['message']

    # Ensure you have your OpenAI API key set in your Flask app's config
    openai.api_key = app.config['OPENAI_API_KEY']

    try:
        # Make a call to OpenAI API with the user's message
        response = openai.Completion.create(
            engine=app.config['OPENAI_ENGINE'],  # Use the engine set in config
            prompt=user_message,
            max_tokens=150
        )
        # Extract the text of the first response
        bot_response = response.choices[0].text.strip()
        return jsonify({'bot_response': bot_response})
    except Exception as e:
        # Handle exceptions, such as errors in communicating with OpenAI API
        print(f"Error while calling OpenAI API: {e}")
        return jsonify({'bot_response': 'Sorry, I am having trouble understanding that.'}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
