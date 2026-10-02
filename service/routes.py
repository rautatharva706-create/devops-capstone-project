"""
Routes for Account Microservice
This module defines the RESTful endpoints for CRUD actions on Customer Accounts.
"""
from flask import Blueprint, jsonify, request, make_response, abort
from service.models import Account, DataValidationError
from service import db

# Create a Flask Blueprint for all API routes
api = Blueprint("api", __name__)

######################################################################
# H O M E   P A G E
######################################################################
@api.route("/", methods=["GET"])
def index():
    """Root URL for the service — returns project details in JSON format"""
    return jsonify({
        "name": "Customer Accounts Microservice",
        "description": "An enterprise-grade RESTful microservice for managing customer accounts.",
        "version": "1.0",
        "endpoints": {
            "list_accounts": "GET /accounts",
            "create_account": "POST /accounts",
            "read_account": "GET /accounts/<id>",
            "update_account": "PUT /accounts/<id>",
            "delete_account": "DELETE /accounts/<id>",
            "health_check": "GET /health"
        }
    }), 200

######################################################################
# H E A L T H   C H E C K
######################################################################
@api.route("/health", methods=["GET"])
def health():
    """Health check endpoint to verify database and app status"""
    return jsonify({"status": "healthy", "service": "accounts"}), 200

######################################################################
# L I S T   A L L   A C C O U N T S
######################################################################
@api.route("/accounts", methods=["GET"])
def list_accounts():
    """Lists all accounts in the database"""
    accounts = Account.all()
    results = [account.serialize() for account in accounts]
    return jsonify(results), 200

######################################################################
# C R E A T E   A   N E W   A C C O U N T
######################################################################
@api.route("/accounts", methods=["POST"])
def create_account():
    """Creates a new customer account based on JSON input"""
    check_content_type("application/json")
    
    data = request.get_json()
    account = Account()
    try:
        account.deserialize(data)
        account.create()
    except DataValidationError as error:
        return jsonify({"error": str(error)}), 400
        
    return jsonify(account.serialize()), 201

######################################################################
# R E A D   A N   A C C O U N T
######################################################################
@api.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Retrieves a specific customer account by its ID"""
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with ID [{account_id}] was not found.")
    return jsonify(account.serialize()), 200

######################################################################
# U P D A T E   A N   E X I S T I N G   A C C O U N T
######################################################################
@api.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Updates an existing account with new data"""
    check_content_type("application/json")
    
    account = Account.find(account_id)
    if not account:
        abort(404, f"Account with ID [{account_id}] was not found.")
        
    data = request.get_json()
    try:
        account.deserialize(data)
        account.update()
    except DataValidationError as error:
        return jsonify({"error": str(error)}), 400
        
    return jsonify(account.serialize()), 200

######################################################################
# D E L E T E   A N   A C C O U N T
######################################################################
@api.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Deletes a customer account by its ID"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204

######################################################################
# U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type of the request matches expectations"""
    if request.headers.get("Content-Type") == content_type:
        return
    abort(415, f"Content-Type must be {content_type}")

######################################################################
# E R R O R   H A N D L E R S
######################################################################
@api.app_errorhandler(404)
def not_found(error):
    """Handles 404 Not Found errors"""
    return jsonify({"status": 404, "error": "Not Found", "message": str(error)}), 404

@api.app_errorhandler(405)
def method_not_allowed(error):
    """Handles 405 Method Not Allowed errors"""
    return jsonify({"status": 405, "error": "Method Not Allowed", "message": str(error)}), 405

@api.app_errorhandler(415)
def unsupported_media_type(error):
    """Handles 415 Unsupported Media Type errors"""
    return jsonify({"status": 415, "error": "Unsupported Media Type", "message": str(error)}), 415

@api.app_errorhandler(500)
def internal_server_error(error):
    """Handles 500 Internal Server Errors"""
    return jsonify({"status": 500, "error": "Internal Server Error", "message": str(error)}), 500
