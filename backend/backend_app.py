from flask_cors import CORS
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from backend.auth import register_user, login_user, token_required
from flask_limiter.util import get_remote_address
from flasgger import Swagger
from utils import load_posts, save_post, update_post_db, delete_post_db, like_post_db, validate_post_data
from rate_limit import limiter
from translations_db import init_db, get_translation, save_translation, session, translate_post
from backend.models import Post, User
import os
from v2_routes import v2 as v2_blueprint



print("Using DB path:", os.path.abspath('blog.db'))
init_db()

# 👇 Function for Identification (user or IP) managing separate limiting
def get_token_or_ip():
    return request.headers.get("Authorization") or get_remote_address()


# locate backend and frontend dirs
HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.abspath(os.path.join(HERE, "..", "frontend"))

app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND, "static"),
    template_folder=FRONTEND
)

# Load config values
app.config["ENV"] = os.getenv("ENV")
app.config["EMAIL_FROM"] = os.getenv("EMAIL_FROM")
app.config["SMTP_SERVER"] = os.getenv("SMTP_SERVER")
app.config["SMTP_PORT"] = int(os.getenv("SMTP_PORT", 587))  # ensure int
app.config["SMTP_USERNAME"] = os.getenv("SMTP_USERNAME")
app.config["SMTP_PASSWORD"] = os.getenv("SMTP_PASSWORD")

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.register_blueprint(v2_blueprint, url_prefix="/api/v2")
app.config['SWAGGER'] = {
    "title": "The Quiet Almanac API",
    "uiversion": 3,
    "description": "A versioned Flask-based blog API with token authentication, rate limiting, and Swagger docs.",
    "version": "2.0",
    "swagger_ui": True,
}
Swagger(app)
CORS(app, origins="*", supports_credentials=True, allow_headers=["Content-Type", "Authorization"])
limiter.init_app(app)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    static_path = os.path.join(app.static_folder, path)
    if path and os.path.exists(static_path):
        return app.send_static_file(path)
    return render_template("index.html")

@app.route("/api/v1/posts", methods=["GET"])
@limiter.exempt
def get_posts():
    posts = load_posts()

    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "desc")
    category = request.args.get("category")
    categories = request.args.get("categories")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 1000))

    if category:
        posts = [p for p in posts if p["category"].lower() == category.lower()]
    elif categories:
        cats = [c.strip().lower() for c in categories.split(",")]
        posts = [p for p in posts if p["category"].lower() in cats]

    if sort_field:
        if sort_field not in ["title", "content", "likes", "date", "updated", "author"]:
            return jsonify({"error": "Invalid sort field."}), 400
        if direction not in ["asc", "desc"]:
            return jsonify({"error": "Invalid direction."}), 400
        reverse = direction == "desc"
        posts.sort(key=lambda p: (p.get(sort_field, "") or "").lower() if isinstance(p.get(sort_field), str) else p.get(sort_field, ""), reverse=reverse)

    start = (page - 1) * limit
    end = start + limit
    paginated = posts[start:end]

    lang = request.args.get("lang", "en").lower()
    if lang != "en":
        for post in paginated:
            trans = get_translation(post["id"], lang)
            if trans:
                post["title"] = trans.title
                post["content"] = trans.content
            else:
                post["title"], post["content"] = translate_post(post["title"], post["content"], lang)
                save_translation(post["id"], lang, post["title"], post["content"])

    return jsonify({"page": page, "limit": limit, "total_posts": len(posts), "posts": paginated})

@app.route("/api/v1/posts", methods=["POST"])
@token_required
@limiter.limit("5 per minute")
def add_post(current_user):
    data = request.get_json()
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    new_post = {
        "author": current_user,
        "title": data["title"],
        "content": data["content"],
        "category": data["category"],
        "likes": 0
    }
    post_id = save_post(new_post)
    new_post["id"] = post_id
    new_post["date"] = datetime.now().strftime("%B %d, %Y")
    return jsonify(new_post), 201

@app.route("/api/v1/posts/<int:post_id>", methods=['PUT'])
@limiter.limit("5 per minute")
@token_required
def update_post(current_user, post_id):
    new_data = request.get_json()
    error = validate_post_data(new_data)
    if error:
        return jsonify(error), 400

    updated_post = update_post_db(post_id, current_user, new_data)
    if updated_post == "unauthorized":
        return jsonify({"error": "Unauthorized to edit this post"}), 403
    elif updated_post is None:
        return jsonify({"error": f"Post with ID {post_id} not found"}), 404

    return jsonify(updated_post), 200

@app.route("/api/v1/posts/<int:post_id>", methods=['DELETE'])
@token_required
@limiter.limit("5 per minute")
def delete_post(current_user, post_id):
    result = delete_post_db(post_id, current_user)
    if result == "unauthorized":
        return jsonify({"error": "Unauthorized to delete this post"}), 403
    elif result == "not_found":
        return jsonify({"error": f"Post with ID {post_id} not found"}), 404
    return jsonify({"message": f"Post {post_id} deleted"}), 200

@app.route("/api/v1/posts/<int:post_id>/like", methods=["POST"])
@limiter.limit("20 per minute")
def like_post(post_id):
    updated_likes = like_post_db(post_id)
    if updated_likes is None:
        return jsonify({"error": f"Post with ID {post_id} not found"}), 404
    return jsonify({"message": f"Post {post_id} liked", "likes": updated_likes}), 200

@app.route("/api/v1/posts/search", methods=['GET'])
@limiter.limit("10 per minute")
def search_post():
    q = (
            request.args.get("q") or
            request.args.get("title") or
            request.args.get("content") or
            ""
    ).strip().lower()
    if not q:
        return jsonify({"error": "Please provide a search term using '?q=your_query'"}), 400

    results = session.query(Post).filter(
        (Post.title.ilike(f"%{q}%")) |
        (Post.content.ilike(f"%{q}%")) |
        (Post.author.ilike(f"%{q}%"))
    ).all()

    if not results:
        return jsonify({"error": f"No posts found matching '{q}'"}), 404

    posts = [{
        "id": post.id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "date": post.date.strftime("%B %d, %Y") if post.date else None,
        "updated": post.updated.strftime("%B %d, %Y") if post.updated else None,
        "likes": post.likes
    } for post in results]

    return jsonify(posts), 200

@app.route("/api/v1/categories", methods=["GET"])
@limiter.exempt
def get_categories():
    categories = session.query(Post.category).distinct().all()
    unique_categories = sorted({c[0] for c in categories if c[0]})
    return jsonify(unique_categories)

@app.route("/api/v1/register", methods=["POST"])
@limiter.limit("3 per minute")
def register():
    return register_user()

@app.route("/api/v1/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    return login_user()

@app.route('/api/v1/secret', methods=['GET'])
@token_required
@limiter.limit("3 per minute")
def secret(current_user):
    return jsonify({'message': f'Welcome, {current_user}!'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5021))
    app.run(host="0.0.0.0", port=port, debug=True)
