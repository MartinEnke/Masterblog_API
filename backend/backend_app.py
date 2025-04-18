from flask_cors import CORS
import json
from datetime import datetime
from flask import Flask, request, jsonify
from auth import register_user, login_user, token_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from v2_routes import v2
from flasgger import Swagger


# 👇 Function for Identification (user or IP)
def get_token_or_ip():
    """Returns either the Authorization token or the IP address as a fallback."""
    return request.headers.get("Authorization") or get_remote_address()


app = Flask(__name__, static_folder="static")
app.register_blueprint(v2)  # v2_routes
app.config['SWAGGER'] = {
    "title": "The Quiet Almanac API",
    "uiversion": 3,
    "description": "📚 A blog API with versioning, rate limiting, and user-auth.",
    "version": "2.0",
    "swagger_ui": True,
}
Swagger(app)
# 👇 Enables Cross-Origin Resource Sharing for *all* routes and *all* methods
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
# 👇 Activate Rate Limiting (works on all functions and routes below)
limiter = Limiter(
    key_func=get_token_or_ip,  # avoids blocking of users sharing an IP-address (f.e. in Cafés)
    app=app,                   # if logged in - token is used, logged out - ip is used
    default_limits=["100 per hour"]
)
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["100 per hour"]
# )


def load_posts():
    """Loads all blog posts from a JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists("blog_posts.json"): # fall back if json doesn't exist
        return []
    with open("blog_posts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    """Saves the current list of blog posts to a JSON file."""
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)


@app.route("/", methods=['GET'])
@limiter.exempt
def home():
    """Health check route for testing the API server."""
    return "Hello, FLASK API"


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


@app.route("/api/v1/posts", methods=["GET"])
@limiter.exempt # Define Stop Limiting (maybe for all GET requests)
def get_posts():
    """Returns a paginated and optionally filtered/sorted list of blog posts."""
    POSTS = load_posts()
    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")
    category = request.args.get("category")
    categories = request.args.get("categories")

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    filtered_posts = POSTS.copy()

    if category:
        filtered_posts = [p for p in filtered_posts if p["category"].lower() == category.lower()]
    elif categories:
        category_list = [c.strip().lower() for c in categories.split(",")]
        filtered_posts = [p for p in filtered_posts if p["category"].lower() in category_list]

    if sort_field:
        valid_fields = ["title", "content", "likes", "date", "updated", "author"]  # ✅ include "author"
        if sort_field not in valid_fields:
            return jsonify({"error": f"Invalid sort field. Use one of: {', '.join(valid_fields)}"}), 400
        if direction not in ["asc", "desc"]:
            return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

        reverse = direction == "desc"
        filtered_posts.sort(
            key=lambda post: (
                post.get(sort_field, "").lower() if isinstance(post.get(sort_field), str)
                else post.get(sort_field, "")
            ),
            reverse=reverse
        )

    start = (page - 1) * limit
    end = start + limit
    paginated_posts = filtered_posts[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": len(filtered_posts),
        "posts": paginated_posts
    })


@app.route('/api/v1/posts', methods=['POST'])
@token_required
@limiter.limit("5 per minute") # Allows productive work but prevents Spam
def add_post(current_user):
    """Creates a new blog post for the logged-in user."""
    POSTS = load_posts()
    data = request.get_json()

    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    new_post = {
        "id": max([post["id"] for post in POSTS], default=0) + 1,
        "author": current_user,  # 🧠 use username from token
        "title": data["title"],
        "content": data["content"],
        "category": data["category"],
        "date": datetime.now().strftime("%B %d, %Y"),
        "likes": 0
    }

    POSTS.append(new_post)
    save_posts(POSTS)

    return jsonify(new_post), 201


@app.route("/api/v1/posts/<int:post_id>", methods=['DELETE'])
@token_required
@limiter.limit("5 per minute") # Allows productive work but prevents Spam
def delete_post(current_user, post_id):
    """Deletes a blog post if it belongs to the current user."""
    POSTS = load_posts()
    for post in POSTS:
        if post['id'] == post_id:
            if post['author'] != current_user:
                return jsonify({"error": "Unauthorized to delete this post"}), 403
            POSTS.remove(post)
            save_posts(POSTS)
            return jsonify({"message": f"Post {post_id} deleted"}), 200
    return jsonify({"error": f"Post with ID {post_id} not found"}), 404


@app.route("/api/v1/posts/<int:post_id>", methods=['PUT'])
@limiter.limit("5 per minute") # Allows productive work but prevents Spam
@token_required
def update_post(current_user, post_id):
    """Updates a blog post's title, content, or category if user owns the post."""
    POSTS = load_posts()
    for post in POSTS:
        if post['id'] == post_id:
            if post['author'] != current_user:
                return jsonify({"error": "Unauthorized to edit this post"}), 403

            new_data = request.get_json()
            error = validate_post_data(new_data)
            if error:
                return jsonify(error), 400

            post['title'] = new_data['title']
            post['content'] = new_data['content']
            post['category'] = new_data['category']
            post["updated"] = datetime.now().strftime("%B %d, %Y")

            save_posts(POSTS)
            return jsonify(post), 200
    return jsonify({"error": f"Post with ID {post_id} not found"}), 404


@app.route("/api/v1/posts/search", methods=['GET'])
@limiter.limit("10 per minute")
def search_post():
    """Searches posts by title, content, or author."""
    POSTS = load_posts()
    search_text = request.args.get("q", "").lower()

    if not search_text:
        return jsonify({"error": "Please provide a search term using '?q=your_query'"}), 400

    results = [
        post for post in POSTS
        if search_text in post.get('title', '').lower()
        or search_text in post.get('content', '').lower()
        or search_text in post.get('author', '').lower()
    ]

    if not results:
        return jsonify({"error": f"No posts found matching '{search_text}'"}), 404

    return jsonify(results), 200


@app.route("/api/v1/categories", methods=["GET"])
@limiter.exempt
def get_categories():
    """Returns a unique sorted list of all categories in blog posts."""
    posts = load_posts()
    categories_set = set()

    for post in posts:
        cat = post.get("category")
        if isinstance(cat, list):
            categories_set.update(cat)
        elif isinstance(cat, str):
            categories_set.add(cat)

    categories = sorted(categories_set)
    return jsonify(categories)


@app.route("/api/v1/posts/<int:post_id>/like", methods=["POST"])
@limiter.limit("20 per minute") # Potential abuse, limiting required, as well
def like_post(post_id):
    """Increments the like count of a post by its ID."""
    posts = load_posts()

    for post in posts:
        if post["id"] == post_id:
            post["likes"] = post.get("likes", 0) + 1
            save_posts(posts)
            return jsonify({"message": f"Post {post_id} liked", "likes": post["likes"]}), 200

    return jsonify({"error": f"Post with ID {post_id} not found"}), 404


'''Register & Login Part'''
@app.route("/api/v1/register", methods=["POST"])
@limiter.limit("3 per minute") # Vulnerable for Brute-Force-Attacks
def register():
    """Registers a new user with username and password."""
    return register_user()


@app.route("/api/v1/login", methods=["POST"])
@limiter.limit("5 per minute") # Vulnerable for Brute-Force-Attacks
def login():
    """Authenticates a user and returns a token."""
    return login_user()


# Debug/Test-Route
@app.route('/api/v1/secret', methods=['GET'])
@token_required
@limiter.limit("3 per minute")
def secret(current_user):
    """Protected test route to verify token authentication."""
    return jsonify({'message': f'Welcome, {current_user}!'}), 200


@app.route('/swagger-ui/custom.css')
def swagger_custom_css():
    """
        Serve the custom Swagger UI stylesheet.

        This route provides a custom CSS file to override or enhance the default
        styling of the Swagger UI. It's typically referenced in the Swagger config
        via the `swagger_ui_css` key to apply branding, layout changes, or visual improvements.

        Returns:
            Response: The static CSS file 'swagger_custom.css' from the Flask static folder.
        """
    return app.send_static_file('swagger_custom.css')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5021, debug=True)
