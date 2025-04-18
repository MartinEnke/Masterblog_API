from flask import jsonify
import os
import json

def load_posts():
    """
    Loads blog posts from blog_posts.json.
    Returns a list of posts or a Flask response if file is invalid.
    """
    if not os.path.exists("blog_posts.json"):
        return []

    try:
        with open("blog_posts.json", "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return jsonify({"error": "Server data is corrupted. Please contact support."}), 500