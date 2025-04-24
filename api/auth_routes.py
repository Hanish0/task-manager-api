from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.auth_models import create_user, authenticate_user
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth_bp', __name__)

class UserSchema(Schema):
    username = fields.Str(required= True)
    password = fields.Str(required = True)
    
user_schema = UserSchema()

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The username
            password:
              type: string
              description: The password
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input data or username already exists
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        errors = user_schema.validate(data)
        if errors:
            return jsonify({"error": "validation error", "details": errors}),400
        username = data.get('username')
        password = data.get('password')

        user_id = create_user(username, password)
        if not user_id:
            return jsonify({"error": "username already exits"}), 400
        
        return jsonify({"message": "user registered successfully", "id": user_id}), 201
    
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
    

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    Login to get access token
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: The username
            password:
              type: string
              description: The password
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "no data provided"}), 400
        username = data.get('username')
        password = data.get('password')

        user = authenticate_user(username, password)
        if not user:
            return jsonify({"error": "Invalid username or password"}), 401
        
        # Create the access token
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

@auth_bp.route('/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected test endpoint
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Access granted
      401:
        description: Missing or invalid token
    """
    current_user = get_jwt_identity()
    return jsonify({"message": f"Protected resource accessed by {current_user}"}), 200