import jwt
from flask import request, jsonify, current_app
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import User
from backend.db import session
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
import re


TOKENS = {}

def is_strong_password(password):
    # Minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 digit, 1 special char
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def validate_login(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return False, {"error": "Invalid username or password"}, 401
    return True, {}, 200

def validate_registration(username, password, email=None):
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        return False, {"error": "User already exists"}, 400

    if not is_strong_password(password):
        return False, {
            "error": "Password is not strong enough. It must be at least 8 characters long, include uppercase, lowercase, digit and special character."
        }, 400

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw, email=email)
    session.add(new_user)
    session.commit()
    return True, {}, 201

def generate_jwt(username):
    payload = {
        "sub": username.strip().lower(),
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise Exception("Token expired")
    except InvalidTokenError:
        raise Exception("Invalid token")


def register_user():
    data = request.get_json() or {}
    username = data.get("username", "").strip().lower()
    email = data.get("email", "").strip().lower() or None  # Optional
    ok, resp, code = validate_registration(username, data.get("password"), email=email)
    if not ok:
        return resp, code
    return {"message": "User registered successfully"}, code

def login_user():
    data = request.get_json() or {}
    username = data.get("username", "").strip().lower()  # ✅ Normalize
    ok, resp, code = validate_login(username, data.get("password"))
    if not ok:
        return resp, code

    token = generate_jwt(data["username"])
    return {"message": "Login successful", "token": token}, 200

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Authentication required"}), 401

        try:
            payload = decode_jwt(token)
            username = payload["sub"]  # you stored it as 'sub'
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        user = session.query(User).filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 401

        return f(user, *args, **kwargs)
    return decorated
