import json
import os
from flask import request, jsonify
from functools import wraps

USERS_FILE = "users.json"
TOKENS = {}  # session-like storage

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def validate_login(username, password):
    users = load_users()
    if username not in users or users[username] != password:
        return False, {"error": "Invalid username or password"}, 401
    return True, {"message": "Login successful", "token": username}, 200

def validate_registration(username, password):
    users = load_users()
    if username in users:
        return False, {"error": "User already exists"}, 400
    users[username] = password
    save_users(users)
    return True, {"message": "User registered successfully"}, 201

# Flask route wrappers
def login_user():
    data = request.get_json()
    return validate_login(data.get("username"), data.get("password"))[1:]

def register_user():
    data = request.get_json()
    return validate_registration(data.get("username"), data.get("password"))[1:]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token not in TOKENS:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated