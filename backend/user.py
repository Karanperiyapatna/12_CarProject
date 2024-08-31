from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__)

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import jwt
import datetime
from auth import token_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'

mongo = PyMongo(app)
CORS(app)

@app.route('/user_signup', methods=['POST'])
def user_signup():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    mongo.db.users.insert_one({
        'username': data['username'],
        'password': hashed_password
    })
    return jsonify({'message': 'User created successfully!'}), 201

@app.route('/user_login', methods=['POST'])
def user_login():
    data = request.json
    user = mongo.db.users.find_one({'username': data['username']})
    if user and check_password_hash(user['password'], data['password']):
        token = jwt.encode({'user': data['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials!'}), 401


@app.route('/user_dashboard', methods=['GET'])
@token_required
def user_dashboard(current_user):
    return jsonify({'message': f'Welcome {current_user} to your dashboard!'})


# @user_bp.route('/user_dashboard')
# def user_dashboard():
#     return render_template('user_dashboard.html')
