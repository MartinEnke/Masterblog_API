from flask import Blueprint, jsonify, request
from flasgger import swag_from
from datetime import datetime
from sqlalchemy.orm import joinedload
from db import session
from models import Post, User, Comment
from rate_limit import limiter
from auth import token_required, register_user, login_user
from utils import validate_post_data

v2 = Blueprint("v2", __name__, url_prefix="/api/v2")


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

@limiter.exempt
def get_posts_v2():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")
    category = request.args.get("category")
    categories = request.args.get("categories")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    query = session.query(Post).options(joinedload(Post.user))

    if category:
        query = query.filter(Post.category.ilike(category))
    elif categories:
        cat_list = [c.strip() for c in categories.split(",")]
        query = query.filter(Post.category.in_(cat_list))

    if sort_field:
        sort_column = getattr(Post, sort_field, None)
        if sort_column is not None:
            query = query.order_by(sort_column.desc() if direction == "desc" else sort_column.asc())

    total_posts = query.count()
    posts = query.offset((page - 1) * limit).limit(limit).all()

    posts_data = [{
        "id": p.id,
        "author": p.user.username,
        "title": p.title,
        "content": p.content,
        "category": p.category,
        "date": p.date.strftime("%B %d, %Y") if p.date else None,
        "updated": p.updated.strftime("%B %d, %Y") if p.updated else None,
        "likes": p.likes
    } for p in posts]

    return jsonify({"page": page, "limit": limit, "total_posts": total_posts, "posts": posts_data})


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
@limiter.limit("5 per minute")  # Allows productive work but prevents spam
def add_post_v2(current_user):
    data = request.get_json()
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    user = session.query(User).filter_by(username=current_user).first()
    if not user:
        return jsonify({"error": "Invalid user"}), 403

    new_post = Post(
        user_id=user.id,
        title=data["title"],
        content=data["content"],
        category=data["category"],
        date=datetime.now(),
        likes=0
    )
    session.add(new_post)
    session.commit()

    return jsonify({
        "id": new_post.id,
        "author": current_user,
        "title": new_post.title,
        "content": new_post.content,
        "category": new_post.category,
        "date": new_post.date.strftime("%B %d, %Y"),
        "likes": new_post.likes
    }), 201


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
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post.author != current_user:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    post.title = data["title"]
    post.content = data["content"]
    post.category = data["category"]
    post.updated = datetime.now()

    session.commit()
    return jsonify({
        "message": "Post updated",
        "post": {
            "id": post.id,
            "author": post.author,
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "date": post.date.strftime("%B %d, %Y") if post.date else None,
            "updated": post.updated.strftime("%B %d, %Y") if post.updated else None,
            "likes": post.likes
        }
    }), 200


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
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if post.author != current_user:
        return jsonify({"error": "Unauthorized"}), 403

    session.delete(post)
    session.commit()
    return jsonify({"message": "Post deleted"}), 200


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
    categories = session.query(Post.category).distinct().all()
    return jsonify(sorted([c[0] for c in categories if c[0]]))


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
    query = (
            request.args.get("q") or
            request.args.get("title") or
            request.args.get("content") or
            ""
    ).strip().lower()
    if not query:
        return jsonify({"error": "Missing query parameter `q`"}), 400

    posts = session.query(Post).options(joinedload(Post.user)).all()
    results = [
        {
            "id": p.id,
            "author": p.user.username,
            "title": p.title,
            "content": p.content,
            "category": p.category,
            "date": p.date.strftime("%B %d, %Y") if p.date else None,
            "updated": p.updated.strftime("%B %d, %Y") if p.updated else None,
            "likes": p.likes
        }
        for p in posts
        if query in p.title.lower() or query in p.content.lower() or query in p.user.username.lower()
    ]

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
@limiter.limit("20 per minute")
def like_post_v2(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": f"Post with ID {post_id} not found"}), 404

    post.likes = post.likes + 1
    session.commit()
    return jsonify({"message": f"Post {post_id} liked", "likes": post.likes}), 200


@v2.route("/posts/<int:post_id>/comments", methods=["POST"])
def add_comment_v2(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "Comment text required"}), 400

    comment = Comment(
        post_id=post.id,
        author=data.get("author", "Anonymous"),
        text=data["text"],
        date=datetime.now()
    )

    session.add(comment)
    session.commit()

    return jsonify({
        "message": "Comment added",
        "comment": {
            "author": comment.author,
            "text": comment.text,
            "date": comment.date.strftime("%B %d, %Y")
        }
    }), 201


@v2.route("/posts/<int:post_id>/comments", methods=["GET"])
def get_comments_v2(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comments = session.query(Comment).filter_by(post_id=post_id).order_by(Comment.date.asc()).all()
    return jsonify([
        {
            "author": c.author,
            "text": c.text,
            "date": c.date.strftime("%B %d, %Y")
        }
        for c in comments
    ])


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
