from flask import Blueprint, jsonify, request
from app.model.users import User
from app.pre_require import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash
from datetime import timedelta

user_bp = Blueprint('user_bp', __name__)
bcrypt = Bcrypt()

def encode_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hash_password, password):
    return bcrypt.check_password_hash(hash_password, password)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

@user_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    print(request)

    if not data or not 'username' in data or not 'email' in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    new_user = User(username=data['username'], email=data['email'],first_name = data['first_name'], last_name = data['last_name'], contact = data['contact'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    if not data or not 'username' in data or not 'email' in data:
        return jsonify({'error': 'Invalid input'}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    user.username = data['username']
    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.contact = data['contact']
    db.session.commit()

    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200


# @user_bp.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if user is None:
#         return jsonify({'error': 'User not found'}), 404
    
#     db.session.delete(user)
#     db.session.commit()

#     return jsonify({'message': 'User deleted successfully'}), 200

@user_bp.route('/users/login', methods=['POST'])
def login():
    password = request.json.get('password')
    email = request.json.get('email')

    user_data = User.query.filter_by(email=email).first()
    print(user_data)
    if user_data and check_password(hash_password=user_data.password,password=password):
        additional_claims= {
            "user_id": user_data.id,
            "username": user_data.username,
            "email": user_data.email
        }

        access_token = create_access_token(identity=str(user_data.id), expires_delta=timedelta(hours=24),additional_claims=additional_claims)
        user_info = {
            "user":additional_claims,
            "access_token":access_token 
        }
        return jsonify(user_info), 200
    else:
        return jsonify({"message":"login unsuccessful"}), 401

@user_bp.route('/users/register', methods=['POST'])
def register():
    username =request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    contact = request.json.get('contact')

    is_user_exist = User.query.filter((User.username == username) | (User.email == email)).first()

    if is_user_exist:
        return jsonify({"message":"User already exists"}),400
    
    hash_password = generate_password_hash(password).decode("utf-8")
    new_user = User(username=username,email=email,password=hash_password,first_name=first_name,last_name=last_name,contact=contact)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"User registered successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":"Procedure failed","info":str(e)}), 500


@user_bp.route('/users/me',methods=['POST'])
@jwt_required()
def me_details():
    user_id = get_jwt_identity()
    
    user_data = User.query.filter_by(id=user_id).first()

    if user_data:
        user_info = {
            "id": user_data.id,
            "username": user_data.username,
            "email": user_data.email
        }
        return jsonify(user_info), 200
    else:
        return jsonify({"message":"User not found"}), 404