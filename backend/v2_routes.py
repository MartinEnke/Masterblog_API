from flask import Blueprint, jsonify, request
from flasgger import swag_from
import json
from datetime import datetime
from utils import load_posts

from Masterblog_API.backend.auth import token_required

v2 = Blueprint("v2", __name__, url_prefix="/api/v2")


'''
This Swagger doc uses "Flasgger" instead of "flask_swagger_ui setup".
Flasgger is more tightly integrated into Flask apps and more maintainable and powerful long term.
It follows the OpenAPI 2.0 spec but integrates Swagger directly via decorators. 
It avoids manual maintenance of a separate JSON file like masterblog.json.
Instead of a static json file it uses Python decorators + @swag_from({...}):.
This is dynamic documentation, written next to the actual route logic, and will stay up to date.

Flasgger vs. swagger_ui setup 

Feature	                        Flasgger                    swagger_ui setup 
🔄 Auto sync with routes	    ✅ Yes (@swag_from)	        ❌ No
🧩 Blueprint-based API design	✅ Modular (v2 blueprint)	❌ Monolithic
✍️ Detailed field schema	    ✅ JSON schema for posts	❌ Very basic
📈 Pagination, sorting, etc.	✅ Documented in Swagger	❌ Missing
🔐 Auth-based logic	            🚧 Partial (planned)	    ❌ None
'''

# -------------------------
# 🔧 Utility functions
# -------------------------

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
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

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
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts
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


@v2.route("/posts/<int:post_id>", methods=["PUT"])
@swag_from({
    "tags": ["Posts"],
    "summary": "Update a blog post",
    "description": "Updates the content of an existing blog post. Requires authentication and ownership.",
    "parameters": [
        {
            "name": "post_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "The ID of the post to update"
        },
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
        200: {"description": "Post updated successfully", "schema": post_schema},
        400: {"description": "Invalid request"},
        403: {"description": "Not authorized"},
        404: {"description": "Post not found"}
    }
})
def update_post_v2(post_id):
    # (basic version without auth for now)
    posts = load_posts()
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

    for post in posts:
        if post['id'] == post_id:
            data = request.get_json()
            if not data or not all(data.get(k) for k in ["title", "content", "category"]):
                return jsonify({"error": "Missing fields"}), 400

            post.update({
                "title": data["title"],
                "content": data["content"],
                "category": data["category"],
                "updated": datetime.now().strftime("%B %d, %Y")
            })
            save_posts(posts)
            return jsonify(post), 200
    return jsonify({"error": "Post not found"}), 404


@v2.route("/posts/<int:post_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Posts"],
    "summary": "Delete a blog post",
    "description": "Deletes a blog post. Requires authentication and ownership.",
    "parameters": [
        {
            "name": "post_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the post to delete"
        }
    ],
    "responses": {
        200: {"description": "Post deleted successfully"},
        403: {"description": "Not authorized to delete this post"},
        404: {"description": "Post not found"}
    }
})
def delete_post_v2(post_id):
    posts = load_posts()
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            save_posts(posts)
            return jsonify({"message": f"Post {post_id} deleted"}), 200
    return jsonify({"error": "Post not found"}), 404


@v2.route("/categories", methods=["GET"])
@swag_from({
    "tags": ["Categories"],
    "summary": "Get all blog post categories",
    "description": "Returns a list of all categories currently used by blog posts.",
    "responses": {
        200: {
            "description": "List of unique categories",
            "schema": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
})
def get_categories_v2():
    posts = load_posts()
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

    categories = sorted({p["category"] for p in posts if p.get("category")})
    return jsonify(categories)


@v2.route("/posts/search", methods=["GET"])
@swag_from({
    "tags": ["Posts"],
    "summary": "Search posts by keyword",
    "description": "Searches for blog posts by matching text in title, content, or author.",
    "parameters": [
        {
            "name": "q",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "Keyword to search in title, content or author"
        }
    ],
    "responses": {
        200: {
            "description": "List of matching posts",
            "schema": {
                "type": "array",
                "items": post_schema
            }
        },
        404: {
            "description": "No matching posts found"
        }
    }
})
def search_posts_v2():
    posts = load_posts()
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify({"error": "Missing query parameter `q`"}), 400

    results = [p for p in posts if
               query in p.get("title", "").lower() or
               query in p.get("content", "").lower() or
               query in p.get("author", "").lower()]

    if not results:
        return jsonify({"error": f"No posts found matching '{query}'"}), 404

    return jsonify(results)


@v2.route("/posts/<int:post_id>/like", methods=["POST"])
@swag_from({
    "tags": ["Posts"],
    "summary": "Like a post",
    "description": "Increments the like count for a post.",
    "parameters": [
        {
            "name": "post_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the post to like"
        }
    ],
    "responses": {
        200: {
            "description": "Post liked successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "likes": {"type": "integer"}
                }
            }
        },
        404: {
            "description": "Post not found"
        }
    }
})
def like_post_v2(post_id):
    posts = load_posts()
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

    for post in posts:
        if post["id"] == post_id:
            post["likes"] = post.get("likes", 0) + 1
            save_posts(posts)
            return jsonify({"message": f"Post {post_id} liked", "likes": post["likes"]}), 200

    return jsonify({"error": f"Post with ID {post_id} not found"}), 404


@v2.route("/login", methods=["POST"])
@swag_from({
    "tags": ["Auth"],
    "summary": "Login a user",
    "description": "Authenticates a user and returns a token for future requests.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["username", "password"],
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Login successful",
            "schema": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "message": {"type": "string"}
                }
            }
        },
        401: {
            "description": "Invalid username or password"
        }
    }
})
def login_user_v2():
    from auth import login_user
    return login_user()


@v2.route("/secret", methods=["GET"])
@swag_from({
    "tags": ["Auth"],
    "summary": "Get a protected welcome message",
    "description": "Returns a message only if the request includes a valid token.",
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "responses": {
        200: {
            "description": "Authenticated user message",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        },
        401: {
            "description": "Missing or invalid token"
        }
    }
})
@token_required
def secret_v2(current_user):
    return jsonify({"message": f"Welcome, {current_user}!"}), 200
