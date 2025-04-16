from flask_cors import CORS
import json
from datetime import datetime
from flask import Flask, request, jsonify
from auth import register_user, login_user, token_required


app = Flask(__name__)
# Enables Cross-Origin Resource Sharing for *all* routes and *all* methods
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


def load_posts():
    with open("blog_posts.json", "r") as file:
        return json.load(file)


def save_posts(posts):
    with open("blog_posts.json", "w") as file:
        json.dump(posts, file, indent=4)


@app.route("/", methods=['GET'])
def home():
    return "Hello, FLASK API"


def validate_post_data(data):
    if not data:
        return {"error": "Enter a title, content, and category"}
    if not data.get("title"):
        return {"error": "Enter a title"}
    if not data.get("content"):
        return {"error": "Enter content"}
    if not data.get("category"):
        return {"error": "Enter a category"}
    return None


@app.route("/api/posts", methods=["GET"])
def get_posts():
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
        valid_fields = ["title", "content", "likes", "date", "updated"]
        if sort_field not in valid_fields:
            return jsonify({"error": f"Invalid sort field. Use one of: {', '.join(valid_fields)}"}), 400
        if direction not in ["asc", "desc"]:
            return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

        reverse = direction == "desc"
        filtered_posts.sort(
            key=lambda post: post.get(sort_field, "").lower() if isinstance(post.get(sort_field), str) else post.get(
                sort_field, ""), reverse=reverse)

    start = (page - 1) * limit
    end = start + limit
    paginated_posts = filtered_posts[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": len(filtered_posts),
        "posts": paginated_posts
    })


@app.route('/api/posts', methods=['POST'])
@token_required
def add_post():
    POSTS = load_posts()
    data = request.get_json()

    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    new_post = {
        "id": max([post["id"] for post in POSTS], default=0) + 1,
        "author": data["author"],
        "title": data["title"],
        "content": data["content"],
        "category": data["category"],
        "date": datetime.now().strftime("%B %d, %Y"),
        "likes": 0
    }

    POSTS.append(new_post)
    save_posts(POSTS)

    return jsonify(new_post), 201


@app.route("/api/posts/<int:post_id>", methods=['DELETE'])
@token_required
def delete_post(post_id):
    POSTS = load_posts()
    filtered_posts = [post for post in POSTS if post["id"] != post_id]

    if len(filtered_posts) == len(POSTS):
        return jsonify({"error": f"Post with ID {post_id} not found"}), 404

    save_posts(filtered_posts)
    return jsonify({"message": f"Post {post_id} deleted"}), 200


@app.route("/api/posts/<int:post_id>", methods=['PUT'])
@token_required
def update_post(post_id):
    POSTS = load_posts()
    for post in POSTS:
        if post['id'] == post_id:
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


@app.route("/api/posts/search", methods=['GET'])
def search_post():
    POSTS = load_posts()
    search_text = request.args.get("q", "").lower()
    if not search_text:
        return jsonify({"error": "Please provide a search term using '?q=your_query'"}), 400

    results = [
        post for post in POSTS
        if search_text in post['title'].lower() or search_text in post['content'].lower()
    ]

    if not results:
        return jsonify({"error": f"No posts found matching '{search_text}'"}), 404

    return jsonify(results), 200


@app.route("/api/categories", methods=["GET"])
def get_categories():
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


@app.route("/api/posts/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    posts = load_posts()

    for post in posts:
        if post["id"] == post_id:
            post["likes"] = post.get("likes", 0) + 1
            save_posts(posts)
            return jsonify({"message": f"Post {post_id} liked", "likes": post["likes"]}), 200

    return jsonify({"error": f"Post with ID {post_id} not found"}), 404


'''Register & Login Part'''
@app.route("/api/register", methods=["POST"])
def register():
    return register_user()


@app.route("/api/login", methods=["POST"])
def login():
    return login_user()

# Example of how you'd protect a route:
@app.route('/api/secret', methods=['GET'])
@token_required
def secret(current_user):
    return jsonify({'message': f'Welcome, {current_user}!'}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5021, debug=True)
