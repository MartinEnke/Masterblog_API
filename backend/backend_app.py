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


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


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
    global POSTS
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5019, debug=True)
