from flask import Blueprint, jsonify, request
from flasgger import swag_from
import json
from datetime import datetime
from utils import load_posts, validate_post_data
from rate_limit import limiter
from auth import token_required

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
        {"name": "categories", "in": "query", "type": "string", "description": "Filter by multiple categories, comma-separated (e.g., Technology,Science)"},
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
            },
            "examples": {
                "application/json": {
                    "posts": [
                        {
                            "id": 1,
                            "author": "SwaggerUser",
                            "title": "Intro to APIs",
                            "content": "Let's build a cool API.",
                            "category": "Technology",
                            "date": "April 18, 2025",
                            "likes": 12
                        }
                    ]
                }
            }
        }
    }
})

@limiter.exempt # Define Stop Limiting (maybe for all GET requests)
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
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["title", "content", "category"],
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                        "category": {"type": "string"}
                    },
                    "example": {
                        "title": "My first post",
                        "content": "This is a great post",
                        "category": "General"
                    }
                }
            }
        }
    },
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
@token_required
@limiter.limit("5 per minute") # Allows productive work but prevents Spam
def add_post_v2(current_user):
    data = request.get_json()
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

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
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["title", "content", "category"],
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                        "category": {"type": "string"}
                    },
                    "example": {
                        "title": "Updated Post Title",
                        "content": "This is the updated content of the blog post.",
                        "category": "UpdatedCategory"
                    }
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "Post updated successfully",
            "schema": post_schema,
            "examples": {
                "application/json": {
                    "id": 1,
                    "author": "SwaggerUser",
                    "title": "Updated Post Title",
                    "content": "This is the updated content of the blog post.",
                    "category": "UpdatedCategory",
                    "date": "April 17, 2025",
                    "likes": 14,
                    "updated": "April 18, 2025"
                }
            }
        },
        400: {"description": "Invalid request"},
        403: {"description": "Not authorized"},
        404: {"description": "Post not found"}
    }
})
@token_required
@limiter.limit("5 per minute") # Allows productive work but prevents Spam
def update_post_v2(current_user, post_id):
    # (basic version without auth for now)
    posts = load_posts()
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

    for post in posts:
        if post['id'] == post_id:
            new_data = request.get_json()
            error = validate_post_data(new_data)
            if error:
                return jsonify(error), 400

            post.update({
                "title": new_data["title"],
                "content": new_data["content"],
                "category": new_data["category"],
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
        200: {
            "description": "Post deleted successfully",
            "examples": {
                "application/json": {
                    "message": "Post 3 deleted"
                }
            }
        },
        403: {"description": "Not authorized to delete this post"},
        404: {"description": "Post not found"}
    }
})

@token_required
@limiter.limit("5 per minute") # Allows productive work but prevents Spam
def delete_post_v2(current_user, post_id):
    posts = load_posts()
    if isinstance(posts, tuple):  # Handles file corruption, sends error response and status code
        return posts

    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            save_posts(posts)
            return jsonify({"message": f"Post {post_id} deleted successfully"}), 200
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
            },
            "examples": {
                "application/json": ["Technology", "Science", "Philosophy", "Travel"]
            }
        }
    }
})

@limiter.exempt
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
            "description": "Keyword to search in title, content, or author (e.g., 'AI')"
        }
    ],
    "responses": {
        200: {
            "description": "List of matching posts",
            "schema": {
                "type": "array",
                "items": post_schema
            },
            "examples": {
                "application/json": [
                    {
                        "id": 5,
                        "author": "Lee",
                        "title": "Understanding AI",
                        "content": "This post explores the basics of artificial intelligence...",
                        "category": "Technology",
                        "date": "April 10, 2025",
                        "likes": 42
                    }
                ]
            }
        },
        404: {
            "description": "No matching posts found",
            "examples": {
                "application/json": {
                    "error": "No posts matched your search"
                }
            }
        }
    }
})
@limiter.limit("10 per minute")
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
            },
            "examples": {
                "application/json": {
                    "message": "Post 5 liked successfully",
                    "likes": 13
                }
            }
        },
        404: {
            "description": "Post not found",
            "examples": {
                "application/json": {
                    "error": "Post with ID 999 not found"
                }
            }
        }
    }
})
@limiter.limit("20 per minute") # Potential abuse, limiting required, as well
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


from auth import register_user, login_user

# -------------------------
# 🔐 POST /register
# -------------------------

@v2.route("/register", methods=["POST"])
@limiter.limit("3 per minute") # Vulnerable for Brute-Force-Attacks
@swag_from({
    "tags": ["Auth"],
    "summary": "Register a new user",
    "description": "Creates a new user account with a username and password.",
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
                },
                "example": {
                    "username": "new_user",
                    "password": "securepassword123"
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "User registered successfully",
            "examples": {
                "application/json": {
                    "message": "User registered successfully"
                }
            }
        },
        400: {
            "description": "Validation error or username taken",
            "examples": {
                "application/json": {
                    "error": "Username already exists"
                }
            }
        }
    }
})
def register_v2():
    return register_user()


# -------------------------
# 🔐 POST /login
# -------------------------

@v2.route("/login", methods=["POST"])
@limiter.limit("5 per minute") # Vulnerable for Brute-Force-Attacks
@swag_from({
    "tags": ["Auth"],
    "summary": "User login",
    "description": "Authenticates a user and returns a token.",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["username", "password"],
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string"}
                    },
                    "example": {
                        "username": "existing_user",
                        "password": "mypassword123"
                    }
                }
            }
        }
    },
    "responses": {
        200: {
            "description": "Login successful, token returned",
            "examples": {
                "application/json": {
                    "message": "Login successful",
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                }
            }
        },
        401: {
            "description": "Unauthorized – invalid credentials",
            "examples": {
                "application/json": {
                    "error": "Invalid username or password"
                }
            }
        }
    }
})
def login_v2():
    return login_user()


@v2.route("/secret", methods=["GET"])
@token_required
@limiter.limit("3 per minute")
@swag_from({
    "tags": ["Auth"],
    "summary": "Test token authentication",
    "description": "Returns a welcome message if token is valid. Requires a valid Bearer token.",
    "parameters": [
        {
            "name": "Authorization",
            "in": "header",
            "type": "string",
            "required": True,
            "description": "Bearer token (e.g., Bearer YOUR_TOKEN_HERE)"
        }
    ],
    "responses": {
        200: {
            "description": "Token is valid",
            "examples": {
                "application/json": {
                    "message": "Welcome, authenticated user!"
                }
            }
        },
        401: {
            "description": "Invalid or missing token",
            "examples": {
                "application/json": {
                    "error": "Token is missing or invalid"
                }
            }
        }
    }
})
def secret_v2(current_user):
    """Protected route to test token-based authentication."""
    return jsonify({"message": f"Welcome, {current_user}!"}), 200
