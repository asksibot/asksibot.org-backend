from flask import Flask, render_template, request, jsonify
import openai
from config import Config  # Make sure Config is properly imported and set up

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    # Set OpenAI API key here (It's better to get it from your config)
    openai.api_key = app.config['OPENAI_API_KEY']

    # Extract the message from the POST request
    data = request.get_json()
    user_message = data['message']

    try:
        # Make a call to OpenAI API with the user's message using GPT-4
        response = openai.Completion.create(
            model=app.config['OPENAI_ENGINE'],  # Ensure this is set to 'gpt-4' in your Config
            prompt=user_message,
            max_tokens=100,
            temperature=0.7  # Adjust based on the desired creativity
        )

        # Extract the text of the response
        bot_response = response.choices[0].text.strip() if response.choices else "I'm not sure how to respond to that."
    except Exception as e:
        # Handle exceptions, such as errors in communicating with OpenAI API
        print(f"Error while calling OpenAI API: {e}")
        bot_response = 'Sorry, I am having trouble understanding that.'

    return jsonify({'bot_response': bot_response})

@app.route('/generate-image', methods=['POST'])
def generate_image():
    # Extract the prompt from the POST request
    data = request.get_json()
    prompt = data['prompt']

    try:
        # Call DALL·E API to generate an image
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1  # Adjust as needed
        )

        # Directly sending the image data back; adjust based on your handling
        image_data = response.data[0]['url']  # This example assumes the API returns a URL
    except Exception as e:
        print(f"Error while calling DALL·E API: {e}")
        return jsonify({'error': 'Failed to generate image'}), 500

    return jsonify({'image_url': image_data})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
