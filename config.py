import os
from flask import Flask, request, jsonify
from flask_mail import Mail

class Config:
    # Flask and security configurations, mail configurations, and OpenAI configurations
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_for_local_dev')
    MAIL_SERVER = os.environ.get('SMTP_HOST', 'smtp.titan.email')
    MAIL_PORT = int(os.environ.get('SMTP_PORT', 465))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'feedback@asksibot.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'MexicoCity@2024')
    MAIL_USE_SSL = True
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'sk-q0POrG6WEWNKxMAiwuq8T3BlbkFJCZ59p9BTcfndT4AY8qdBS') #changed key 3-27-2024
    OPENAI_ENGINE = os.environ.get('OPENAI_ENGINE', 'gpt-4') #change to GPT-4

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail = Mail(app)

    # Example route for handling OpenAI chatbot requests
    @app.route('/chatbot', methods=['POST'])
    def chatbot():
        user_message = request.json.get('message', '')
        
        from openai import OpenAI
        
        client = OpenAI(api_key=app.config['OPENAI_API_KEY'])

        response = client.chat.completions.create(model=app.config['OPENAI_ENGINE'],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ])

        answer = response.choices[0].message.content.strip() if response.choices else "I'm not sure how to respond to that."

        return jsonify({'answer': answer})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
