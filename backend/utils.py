from flask import jsonify
import os
import json


def validate_post_data(data):
    """Validates required fields in a post dictionary."""
    if not data:
        return {"error": "Enter a title, content, and category"}
    if not data.get("title"):
        return {"error": "Enter a title"}
    if not data.get("content"):
        return {"error": "Enter content"}
    if not data.get("category"):
        return {"error": "Enter a category"}
    return None


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