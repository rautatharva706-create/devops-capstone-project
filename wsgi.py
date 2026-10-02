"""
WSGI Entry Point
This script runs the Customer Accounts Microservice using the Flask development server.
"""
import os
from service import create_app

# Instantiate the Flask app using the factory
app = create_app()

if __name__ == "__main__":
    # Retrieve port from environment, or default to 8080
    port = int(os.getenv("PORT", 8080))
    app.logger.info(f"Starting Accounts Microservice on port {port}...")
    app.run(host="0.0.0.0", port=port)
