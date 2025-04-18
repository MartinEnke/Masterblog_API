import json
import os
from flask import request, jsonify
from functools import wraps

USERS_FILE = "users.json"
TOKENS = {}  # session-like storage


def load_users():
    """
    Loads user credentials from the users.json file.

    Returns:
        dict: A dictionary of users with usernames as keys and passwords as values.
              Returns an empty list if the file does not exist.
    """
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    """
    Saves the given users dictionary to the users.json file.

    Args:
        users (dict): A dictionary of users to save.
    """
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)


def validate_login(username, password):
    """
    Validates a username and password combination.

    Args:
        username (str): The username to validate.
        password (str): The corresponding password.

    Returns:
        tuple: A tuple containing:
            - bool: Whether login is successful.
            - dict: A success message with token or an error message.
            - int: HTTP status code.
    """
    users = load_users()
    if username not in users or users[username] != password:
        return False, {"error": "Invalid username or password"}, 401
    return True, {"message": "Login successful", "token": username}, 200


def validate_registration(username, password):
    """
    Validates and registers a new user.

    Args:
        username (str): Desired username.
        password (str): Desired password.

    Returns:
        tuple: A tuple containing:
            - bool: Whether registration is successful.
            - dict: A success or error message.
            - int: HTTP status code.
    """
    users = load_users()
    if username in users:
        return False, {"error": "User already exists"}, 400
    users[username] = password
    save_users(users)
    return True, {"message": "User registered successfully"}, 201


def login_user():
    """
    Handles a login request by validating user credentials.

    Returns:
        tuple: A tuple containing a response dict and status code.
               If successful, also stores the token in the TOKENS dictionary.
    """
    data = request.get_json()
    success, response, status = validate_login(data.get("username"), data.get("password"))
    if success:
        # ✅ Store the token (username) so @token_required can find it later
        TOKENS[response["token"]] = data.get("username")
    return response, status


def register_user():
    """
    Handles a user registration request.

    Returns:
        tuple: A tuple containing a response dict and status code.
    """
    data = request.get_json()
    return validate_registration(data.get("username"), data.get("password"))[1:]


def token_required(f):
    """
    Decorator that ensures a route is protected by token-based authentication.

    Checks for a valid token in the 'Authorization' header.
    If invalid or missing, returns a 401 Unauthorized response.

    Args:
        f (function): The route function to wrap.

    Returns:
        function: The decorated route function with authentication check.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token or token not in TOKENS:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated
