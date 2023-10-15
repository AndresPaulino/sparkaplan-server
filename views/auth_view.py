# views/auth_view.py
from flask import Blueprint, request, jsonify
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_view = Blueprint('auth_view', __name__)

@auth_view.route('/account/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data['email'])
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(accessToken=access_token, user={"id": user.id, "email": user.email, "firstName": user.first_name, "lastName": user.last_name, "displayName": user.display_name, "county": user.county, "state": user.state})
    
    return jsonify(message="Invalid email or password"), 401

@auth_view.route('/account/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.find_by_email(data['email']):
        return jsonify(message="Email already exists."), 400

    user = User(
        email=data['email'],
        password=User.hash_password(data['password']),
        first_name=data['firstName'],
        last_name=data['lastName'],
        display_name=data['firstName'] + " " + data['lastName']
    )
    user.save_to_db()
    access_token = create_access_token(identity=user.id)
    return jsonify(accessToken=access_token, user={"id": user.id, "email": user.email})

@auth_view.route('/account/my-account', methods=['GET'])
@jwt_required()
def get_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404
    return jsonify(user={"id": user.id, "email": user.email, "firstName": user.first_name, "lastName": user.last_name, "displayName": user.display_name, "county": user.county, "state": user.state})
