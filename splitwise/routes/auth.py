from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..utils.jwt_utils import generate_token, token_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    
    # Basic validation
    if not data.get('email') or '@' not in data.get('email'):
        return jsonify({"error": "Invalid email address"}), 400
    
    email = data.get('email')
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    
    # Create new user
    new_user = User(
        username=data.get('username'),
        email=email
    )
    new_user.set_password(data.get('password'))
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate token
    token = generate_token(new_user.id)
    
    return jsonify({
        "message": "User registered successfully",
        "user_id": new_user.id,
        "token": token
    }), 201

@auth.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and user.check_password(data.get('password')):
        token = generate_token(user.id)
        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "token": token
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """User logout endpoint"""
    return jsonify({"message": "Logged out successfully"}), 200

@auth.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get current user profile"""
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }), 200
