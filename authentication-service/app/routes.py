from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    auth_collection = current_app.auth_collection
    existing_user = auth_collection.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)
    auth_collection.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    auth_collection = current_app.auth_collection
    user = auth_collection.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Generate JWT token
    jwt_secret = current_app.config['JWT_SECRET_KEY']
    jwt_algorithm = current_app.config['JWT_ALGORITHM']
    token = jwt.encode({
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }, jwt_secret, algorithm=jwt_algorithm)
    
    return jsonify({"token": token}), 200
