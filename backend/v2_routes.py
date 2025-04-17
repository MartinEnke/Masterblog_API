from flask import Blueprint, jsonify, request
from flasgger import swag_from
import json
import os
from datetime import datetime

v2 = Blueprint("v2", __name__, url_prefix="/api/v2")

# -------------------------
# 🔧 Utility functions
# -------------------------

def load_posts():
    if not os.path.exists("blog_posts.json"):
        return []
    with open("blog_posts.json", "r") as file:
        return json.load(file)

def save_posts(posts):
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)

# -------------------------
# 📚 Swagger schemas
# -------------------------

post_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "author": {"type": "string"},
        "title": {"type": "string"},
        "content": {"type": "string"},
        "category": {"type": "string"},
        "date": {"type": "string"},
        "likes": {"type": "integer"},
        "updated": {"type": "string"}
    }
}

# -------------------------
# 📘 GET /posts
# -------------------------

@v2.route("/posts", methods=["GET"])
@swag_from({
    "tags": ["Posts"],
    "summary": "Get all blog posts",
    "description": "Returns all blog posts with optional filtering, sorting, and pagination.",
    "parameters": [
        {"name": "category", "in": "query", "type": "string", "description": "Filter by a single category"},
        {"name": "categories", "in": "query", "type": "string", "description": "Filter by multiple categories, comma-separated"},
        {"name": "sort", "in": "query", "type": "string", "enum": ["title", "author", "likes", "date", "updated"], "description": "Sort by field"},
        {"name": "direction", "in": "query", "type": "string", "enum": ["asc", "desc"], "default": "asc", "description": "Sort direction"},
        {"name": "page", "in": "query", "type": "integer", "default": 1, "description": "Page number"},
        {"name": "limit", "in": "query", "type": "integer", "default": 5, "description": "Results per page"}
    ],
    "responses": {
        200: {
            "description": "List of posts",
            "schema": {
                "type": "object",
                "properties": {
                    "posts": {
                        "type": "array",
                        "items": post_schema
                    }
                }
            }
        }
    }
})
def get_posts_v2():
    posts = load_posts()
    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")
    category = request.args.get("category")
    categories = request.args.get("categories")

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    filtered = posts.copy()

    if category:
        filtered = [p for p in filtered if p["category"].lower() == category.lower()]
    elif categories:
        cat_list = [c.strip().lower() for c in categories.split(",")]
        filtered = [p for p in filtered if p["category"].lower() in cat_list]

    if sort_field:
        reverse = direction == "desc"
        filtered.sort(
            key=lambda post: (
                post.get(sort_field, "").lower()
                if isinstance(post.get(sort_field), str)
                else post.get(sort_field, "")
            ),
            reverse=reverse
        )

    start = (page - 1) * limit
    end = start + limit
    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": len(filtered),
        "posts": filtered[start:end]
    })


# -------------------------
# 📝 POST /posts
# -------------------------

@v2.route("/posts", methods=["POST"])
@swag_from({
    "tags": ["Posts"],
    "summary": "Create a new post",
    "description": "Adds a new blog post (requires authentication).",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["title", "content", "category"],
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "category": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "Post successfully created",
            "schema": post_schema
        },
        400: {
            "description": "Validation failed"
        }
    }
})
def add_post_v2():
    data = request.get_json()
    if not data or not all(data.get(k) for k in ["title", "content", "category"]):
        return jsonify({"error": "Please provide title, content, and category"}), 400

    posts = load_posts()
    new_post = {
        "id": max((post["id"] for post in posts), default=0) + 1,
        "author": "SwaggerUser",  # For demo. Replace with actual user in full auth version.
        "title": data["title"],
        "content": data["content"],
        "category": data["category"],
        "date": datetime.now().strftime("%B %d, %Y"),
        "likes": 0
    }
    posts.append(new_post)
    save_posts(posts)
    return jsonify(new_post), 201
