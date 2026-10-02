"""
Service Initialization module
This module initializes the Flask application and sets up core extensions
like SQLAlchemy, CORS, and Talisman for security headers.
"""
import os
import sys
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_talisman import Talisman

# Initialize SQLAlchemy database instance
db = SQLAlchemy()

def create_app():
    """Initializes and returns the Flask application instance"""
    app = Flask(__name__)

    # Set up configuration from environment variables or defaults
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-12345")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", "sqlite:///../development.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Configure CORS - Enable Cross-Origin Resource Sharing
    # Allow all origins for development, but restrict as needed for production
    CORS(app)

    # Configure Talisman for HTTP Security Headers
    # We disable force_https for local development and testing
    talisman = Talisman(
        app,
        content_security_policy={
            'default-src': '\'self\'',
            'object-src': '\'none\''
        },
        force_https=False,
        strict_transport_security=True,
        session_cookie_secure=False
    )

    # Set up logging for output transparency
    app.logger.setLevel(logging.INFO)
    app.logger.info("Initializing the Customer Accounts Microservice...")

    with app.app_context():
        # Import models and routes to register them with the app
        from service.routes import api
        app.register_blueprint(api)
        
        # Create database tables if they do not exist
        try:
            db.create_all()
            app.logger.info("Database tables verified successfully.")
        except Exception as error:
            app.logger.error(f"Error creating database tables: {error}")
            sys.exit(1)

    return app
