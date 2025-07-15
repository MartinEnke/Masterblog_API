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
    """
        Check if the given password meets strength requirements.

        Requirements:
            - Minimum 8 characters
            - At least 1 uppercase letter
            - At least 1 lowercase letter
            - At least 1 digit
            - At least 1 special character (!@#$%^&*(),.?":{}|<>)

        Args:
            password (str): Password string to validate.

        Returns:
            bool: True if password is strong, False otherwise.
        """
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
    """
        Validate user credentials for login.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            tuple:
                bool: True if credentials are valid, False otherwise.
                dict: Error message dict if invalid.
                int: HTTP status code.
        """
    user = session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return False, {"error": "Invalid username or password"}, 401
    return True, {}, 200

def validate_registration(username, password, email=None):
    """
        Validate user registration data and create user if valid.

        Args:
            username (str): Desired username.
            password (str): Password.
            email (str, optional): User's email address.

        Returns:
            tuple:
                bool: True if registration successful, False otherwise.
                dict: Error message dict if invalid.
                int: HTTP status code.
        """
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
    """
        Generate a JWT token for a given username.

        Args:
            username (str): Username to encode in token.

        Returns:
            str: JWT token string.
        """
    payload = {
        "sub": username.strip().lower(),
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def decode_jwt(token):
    """
        Decode and verify a JWT token.

        Args:
            token (str): JWT token string.

        Raises:
            Exception: If token is expired or invalid.

        Returns:
            dict: Decoded JWT payload.
        """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise Exception("Token expired")
    except InvalidTokenError:
        raise Exception("Invalid token")

def register_user():
    """
        Flask route handler to register a new user.

        Expects JSON payload with 'username', 'password', and optional 'email'.

        Returns:
            tuple: JSON response and HTTP status code.
        """
    data = request.get_json() or {}
    username = data.get("username", "").strip().lower()
    email = data.get("email", "").strip().lower() or None  # Optional
    ok, resp, code = validate_registration(username, data.get("password"), email=email)
    if not ok:
        return resp, code
    return {"message": "User registered successfully"}, code

def login_user():
    """
        Flask route handler to authenticate a user and return a JWT token.

        Expects JSON payload with 'username' and 'password'.

        Returns:
            tuple: JSON response containing login message and token, plus HTTP status.
        """
    data = request.get_json() or {}
    username = data.get("username", "").strip().lower()  # ✅ Normalize
    ok, resp, code = validate_login(username, data.get("password"))
    if not ok:
        return resp, code

    token = generate_jwt(data["username"])
    return {"message": "Login successful", "token": token}, 200

def token_required(f):
    """
        Decorator to require JWT authentication for Flask routes.

        Verifies 'Authorization' header for Bearer token, decodes token, and
        loads user from database. Passes the user as first argument to the route.

        Returns:
            function: Decorated function that enforces token authentication.
        """
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
