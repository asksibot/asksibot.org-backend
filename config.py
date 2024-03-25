import os
from flask import Flask
from flask_mail import Mail

class Config:
    # Flask and security configurations
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_for_local_dev')
    
    # Mail configurations updated as per discussion
    MAIL_SERVER = os.environ.get('SMTP_HOST', 'smtp.titan.email')
    MAIL_PORT = int(os.environ.get('SMTP_PORT', 465))  # Assuming SSL encryption
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'feedback@asksibot.com')  # Updated username
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'MexicoCity@2024')  # Updated password
    MAIL_USE_SSL = True  # Using SSL for encryption, not STARTTLS
    # Removed MAIL_USE_TLS since we're defaulting to SSL with port 465, adjust if using port 587

    # OpenAI configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'sk-q0POrG6WEWNKxMAiwuq8T3BlbkFJCZ59p9BTcfndT4AY8qdBS')  # Default key as fallback
    OPENAI_ENGINE = os.environ.get('OPENAI_ENGINE', 'text-davinci-003')  # Default engine as fallback

def create_app():
    app = Flask(__name__)
    
    # Load app configurations from the Config class
    app.config.from_object(Config)
    
    # Initialize Flask-Mail with app's configurations
    mail = Mail(app)

    # Define routes and other app configurations below as needed

    return app, mail
