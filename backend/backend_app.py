from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route("/", methods=['GET'])
def home():
    return "Hello, FLASK API"


def validate_post_data(data):
    '''Reusable data validation'''
    if not data:
        return {"error": "Enter a title and content"}
    if not data.get("title"):
        return {"error": "Enter a title for your content"}
    if not data.get("content"):
        return {"error": "Enter content to your title"}
    return None  # No errors


@app.route("/api/posts", methods=["GET"])
def get_posts():
    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))

    # Copy original list to avoid modifying global state
    sorted_posts = POSTS.copy()

    # If sorting is requested
    if sort_field:
        if sort_field not in ["title", "content"]:
            return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400
        if direction not in ["asc", "desc"]:
            return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

        reverse = direction == "desc"
        sorted_posts.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_posts = sorted_posts[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_posts": len(sorted_posts),
        "posts": paginated_posts
    })


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    # Call data validator
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    new_post = {
        "id": len(POSTS) + 1,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route("/api/posts/<int:post_id>", methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    for post in POSTS:
        if post['id'] == post_id:
            break
    else:
        # This else runs only if the for-loop completes WITHOUT breaking
        return jsonify({"error": f"{post_id} not found"}), 404

    POSTS = [post for post in POSTS if post["id"] != post_id]
    return jsonify({"message": f"Post {post_id} deleted"}), 200


@app.route("/api/posts/<int:post_id>", methods=['PUT'])
def update_post(post_id):
    for post in POSTS:
        if post['id'] == post_id:
            new_data = request.get_json()

            # Call data validator
            error = validate_post_data(new_data)
            if error:
                return jsonify(error), 400

            post['title'] = new_data['title']
            post['content'] = new_data['content']

            return jsonify(post), 200
    return jsonify({"error": f"Post with ID {post_id} not found"}), 404


@app.route("/api/posts/search", methods=['GET'])
def search_post():
    search_text = request.args.get("q", "").lower()
    if not search_text:
        return jsonify({"error": "Please provide a search term using '?q=your_query'"}), 400

    # Find all matches (case-insensitive)
    results = [
        post for post in POSTS
        if search_text in post['title'].lower() or search_text in post['content'].lower()
    ]

    if not results:
        return jsonify({"error": f"No posts found matching '{search_text}'"}), 404

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5019, debug=True)
