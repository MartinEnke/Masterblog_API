
import jwt
from flask import request, jsonify, current_app
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from db import session
from datetime import datetime, timedelta

def validate_login(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return False, {"error": "Invalid username or password"}, 401
    return True, {}, 200

def validate_registration(username, password):
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        return False, {"error": "User already exists"}, 400

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    session.add(new_user)
    session.commit()
    return True, {}, 201

def generate_jwt(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token


def register_user():
    data = request.get_json() or {}
    ok, resp, code = validate_registration(data.get("username"), data.get("password"))
    if not ok:
        return resp, code
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
