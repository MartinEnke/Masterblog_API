import json
import os
import datetime
import jwt
from flask import request, jsonify, current_app
from functools import wraps

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def validate_login(username, password):
    users = load_users()
    if username not in users or users[username] != password:
        return False, {"error": "Invalid username or password"}, 401
    return True, {}, 200

def validate_registration(username, password):
    users = load_users()
    if username in users:
        return False, {"error": "User already exists"}, 400
    users[username] = password
    save_users(users)
    return True, {}, 201

def generate_jwt(username):
    """Create a JWT with a 2-hour expiration."""
    now = datetime.datetime.utcnow()
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def register_user():
    data = request.get_json() or {}
    ok, resp, code = validate_registration(data.get("username"), data.get("password"))
    if not ok:
        return resp, code
    # on success, auto-login could generate a token here if you like
    return {"message": "User registered successfully"}, code

def login_user():
    data = request.get_json() or {}
    ok, resp, code = validate_login(data.get("username"), data.get("password"))
    if not ok:
        return resp, code

    token = generate_jwt(data["username"])
    return {"message": "Login successful", "token": token}, 200

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"error": "Authentication required"}), 401

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        current_user = payload["sub"]
        return f(current_user, *args, **kwargs)

    return decorated
