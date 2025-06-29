from flasgger import swag_from
from datetime import datetime
from sqlalchemy.orm import joinedload
from db import session
from models import Post, User, Comment, PostLike
from rate_limit import limiter
from auth import token_required, register_user, login_user, TOKENS
from utils import load_posts, save_post, update_post_db, delete_post_db, like_post_db, validate_post_data, send_email
from translations_db import get_translation, save_translation, translate_post
from babel.dates import format_date
from langdetect import detect
from traceback import print_exc
from flask import g
import jwt
from flask import current_app
from models import User
from utils import can_call_openai, moderate_post
from openai import OpenAIError
import openai
from sqlalchemy import func
import os, requests, base64
from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from notifications import send_email
import html
import re
from threading import Thread
from utils import send_email
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError

v2 = Blueprint("v2", __name__, url_prefix="/api/v2")


HUME_KEY = os.getenv("HUME_KEY")  # set in .env

@v2.route("/generate-tts", methods=["POST"])
@token_required
def gen_tts_hume(current_user):
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    if current_user.tts_demo_used:
        return jsonify({"error": "TTS demo already used"}), 403

    print(f"🔊 Generating TTS for user: {current_user.username}")

    # Hume API request
    url = "https://api.hume.ai/v0/tts"
    payload = {"utterances": [{"text": text}]}

    try:
        resp = requests.post(url, json=payload, headers={
            "X-Hume-Api-Key": HUME_KEY,
            "Content-Type": "application/json"
        })

        if not resp.ok:
            print("❌ Hume TTS error:", resp.text)
            return jsonify({"error": resp.text}), resp.status_code

        # ✅ Mark demo used and commit
        if not current_user.tts_demo_used:
            current_user.tts_demo_used = True
            session.commit()
            session.expire_all()  # 🔥 Force refresh of session objects

        data = resp.json()
        audio_b64 = data["generations"][0]["audio"]
        mp3_bytes = base64.b64decode(audio_b64)

        return send_file(BytesIO(mp3_bytes), mimetype="audio/mpeg")

    except Exception as e:
        print("🔥 Unexpected error in /generate-tts:", e)
        return jsonify({"error": "Internal server error"}), 500



@v2.route("/tts-demo-status", methods=["GET"])
@token_required
def tts_demo_status(current_user):
    session.refresh(current_user)
    return jsonify({"used_demo": current_user.tts_demo_used})

def get_current_user_from_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        username = payload["sub"]
        return session.query(User).filter_by(username=username).first()
    except Exception as e:
        print("❌ Invalid token:", e)
        return None

def get_user_from_token_value(token):
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        username = payload["sub"]
        return session.query(User).filter_by(username=username).first()
    except Exception as e:
        print("❌ Invalid token:", e)
        return None


@v2.route("/user", methods=["GET"])
@token_required
def get_user(current_user):
    return jsonify({
        "username": current_user.username,
        "email": current_user.email,
        "notifications_enabled": current_user.notifications_enabled
    }), 200


@v2.route("/user/email", methods=["PUT"])
@token_required
def update_email(current_user):
    data = request.get_json()
    new_email = data.get("email")
    notify_pref = data.get("notifications_enabled")  # Optional from frontend

    email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
    if not new_email or not re.match(email_pattern, new_email) or len(new_email) > 254:
        return jsonify({"error": "Invalid email address"}), 400

    current_user.email = new_email

    # ✅ Force notifications ON if a valid email is saved
    current_user.notifications_enabled = True if new_email else False

    try:
        session.commit()
        return jsonify({
            "message": "Email updated",
            "email": new_email,
            "notifications_enabled": current_user.notifications_enabled
        }), 200
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "This email is already in use."}), 409


@v2.route("/user/notifications", methods=["PUT"])
@token_required
def toggle_notification_setting(current_user):
    data = request.get_json()
    enabled = data.get("enabled")

    if enabled not in [True, False]:
        return jsonify({"error": "Invalid 'enabled' value"}), 400

    current_user.notifications_enabled = enabled

    try:
        session.commit()
        return jsonify({
            "message": "Notification preference updated",
            "notifications_enabled": current_user.notifications_enabled
        }), 200
    except Exception as e:
        session.rollback()
        print("❌ Error updating notification setting:", e)
        return jsonify({"error": "Failed to update notification preference."}), 500


# -------------------------
# Swagger schemas
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
# GET /posts
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
    print("✅ /api/v2/posts was called")
    try:
        lang = request.args.get("lang", "en")
        sort_field = request.args.get("sort", "date")
        direction = request.args.get("direction", "desc")
        category = request.args.get("category")
        categories = request.args.get("categories")
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 50))

        current_user = get_current_user_from_token()
        print("🔍 User:", current_user.username if current_user else "None")
        print("🔐 Is admin:", current_user.is_admin if current_user else "N/A")
        is_admin = current_user.is_admin if current_user else False

        query = session.query(Post).options(joinedload(Post.user))

        # 🛡️ Filter out unapproved posts for normal users
        if not is_admin:
            query = query.filter(Post.review_status == "approved")

        if category:
            query = query.filter(Post.category.ilike(category))
        elif categories:
            cat_list = [c.strip() for c in categories.split(",")]
            query = query.filter(Post.category.in_(cat_list))

        posts = query.all()  # ✅ get all results so we can sort and paginate manually
        posts_data = []

        search_term = request.args.get("q", "").strip().lower()

        for p in posts:
            # Default values
            title = p.title
            content = p.content
            is_ai = False
            translated_flag = False

            # 🌐 Load translation if needed
            if lang != p.original_lang:
                translation = get_translation(p.id, lang)
                if translation:
                    title = translation.title
                    content = translation.content
                    translated_flag = True
                    is_ai = getattr(translation, "is_ai_translation", True)
                else:
                    try:
                        title_trans, content_trans = translate_post(p.title, p.content, lang)
                        save_translation(
                            post_id=p.id,
                            lang=lang,
                            title=title_trans,
                            content=content_trans,
                            is_ai=True
                        )
                        title = title_trans
                        content = content_trans
                        translated_flag = True
                        is_ai = True
                    except Exception as e:
                        print(f"⚠️ Failed to translate post {p.id} to {lang}:", e)
                        translated_flag = False
                        is_ai = False
            else:
                translated_flag = True

            # 🔍 Apply search on FINAL text (whether translated or original)
            if search_term:
                if search_term not in title.lower() and search_term not in content.lower():
                    continue

            liked_by_user = False
            if current_user:
                liked_by_user = any(l.user_id == current_user.id for l in p.liked_by)

            posts_data.append({
                "id": p.id,
                "author": p.user.username,
                "title": title,
                "content": content,
                "category": p.category,
                "date": p.date.strftime("%B %d, %Y") if p.date else None,
                "date_sort": p.date.isoformat() if p.date else None,
                "updated": p.updated.strftime("%B %d, %Y") if p.updated else None,
                "likes": len(p.liked_by),
                "translated": translated_flag,
                "is_ai_translation": is_ai,
                "original_lang": p.original_lang,
                "liked_by_current_user": liked_by_user,
                "review_status": p.review_status,
                "is_owner": current_user and current_user.id == p.user_id
            })

        # ✅ Sort posts_data after it's fully built
        if sort_field:
            valid_fields = ["title", "content", "likes", "date", "updated", "author"]
            if sort_field not in valid_fields:
                return jsonify({"error": "Invalid sort field."}), 400
            if direction not in ["asc", "desc"]:
                return jsonify({"error": "Invalid direction."}), 400

            reverse = direction == "desc"

            if sort_field == "likes":
                posts_data.sort(key=lambda p: p.get("likes", 0), reverse=reverse)

            elif sort_field == "updated":
                posts_data.sort(
                    key=lambda p: p.get("updated") or p.get("date_sort") or datetime.min.isoformat(),
                    reverse=reverse
                )

            elif sort_field == "date":
                posts_data.sort(
                    key=lambda p: p.get("date_sort") or datetime.min.isoformat(),
                    reverse=reverse
                )

            else:
                posts_data.sort(
                    key=lambda p: (p.get(sort_field, "") or "").lower()
                    if isinstance(p.get(sort_field), str) else p.get(sort_field, ""),
                    reverse=reverse
                )

        # ✅ Apply pagination AFTER sorting
        total_posts = len(posts_data)
        start = (page - 1) * limit
        end = start + limit
        paginated = posts_data[start:end]

        return jsonify({
            "page": page,
            "limit": limit,
            "total_posts": total_posts,
            "posts": paginated
        })

    except Exception as e:
        import traceback
        print("🔥 ERROR IN /posts:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500




@v2.route("/posts/<int:post_id>/translate")
def translate_individual_post(post_id):
    lang = request.args.get("lang", "en")
    post = session.query(Post).filter_by(id=post_id).first()

    if not post:
        return jsonify({"error": "Post not found"}), 404

    translation = get_translation(post_id, lang)
    if translation:
        return jsonify({
            "title": translation.title,
            "content": translation.content,
            "lang": lang
        })

    # 🛑 Rate-limit OpenAI calls
    if not can_call_openai(limit=10):  # Or whatever per-hour limit you want
        return jsonify({"error": "AI translation limit reached. Try again later."}), 429

    # 🧠 AI translation logic
    from translations_db import translate_post, save_translation
    print(f"🔁 Translating post {post_id} to {lang} using AI")

    new_title, new_content = translate_post(post.title, post.content, lang)
    save_translation(post_id, lang, new_title, new_content)
    session.commit()

    return jsonify({
        "title": new_title,
        "content": new_content,
        "lang": lang
    })
# -------------------------
# POST /posts
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
@limiter.limit("5 per minute")
def add_post_v2(current_user):
    data = request.get_json()

    # ✅ 1. Validate input before doing anything else
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    # ✅ 2. Sanitize and prepare fields
    title = html.escape(data["title"].strip())
    content = html.escape(data["content"].strip())
    category = data["category"].strip()
    ui_lang = data.get("lang", "en")
    date = datetime.now()

    # 🌐 3. Detect original language
    try:
        original_lang = detect(f"{title} {content}")
    except Exception:
        original_lang = "und"

    # ⛔ 4. Rate-limit OpenAI moderation
    if not can_call_openai(limit=10):
        return jsonify({
            "error": "AI moderation temporarily unavailable. Too many requests this hour. Try again later.",
            "remaining_calls": 0
        }), 429

    # 🤖 5. Moderate content using OpenAI
    try:
        review_status = moderate_post(title, content)
    except Exception as e:
        print(f"❌ Moderation error: {e}")
        review_status = "needs_review"

    # 💾 6. Save post to database
    post = Post(
        title=title,
        content=content,
        category=category,
        user_id=current_user.id,
        date=date,
        original_lang=original_lang,
        review_status=review_status
    )
    session.add(post)
    session.commit()

    # 🌍 7. Translate to English if needed (optional for future UI)
    if original_lang != "en":
        try:
            print(f"🌍 Translating post {post.id} from {original_lang} to English")
            title_en, content_en = translate_post(title, content, "en")
            save_translation(post.id, "en", title_en, content_en)
        except Exception as e:
            print(f"⚠️ Translation failed: {e}")

    # ✅ 8. Respond to client
    response = {
        "post_id": post.id,
        "review_status": review_status
    }

    if review_status == "approved":
        response["message"] = "✅ Post added successfully and is now visible to others."
    elif review_status == "needs_review":
        response["message"] = (
            "⚠️ Your post has been flagged for review and is not yet public. "
            "Please be mindful of sensitive or unclear language."
        )
    else:  # rejected
        response["message"] = (
            "🚫 Your post contains inappropriate or harmful language and has been rejected. "
            "It will not be visible to others. Please review our content guidelines."
        )

    if ui_lang != original_lang:
        response["warning"] = f"⚠️ The text appears to be in {original_lang}, not {ui_lang}."

    return jsonify(response), 201





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

    if post.user_id != current_user.id and not getattr(current_user, "is_admin", False):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    error = validate_post_data(data)
    if error:
        return jsonify(error), 400

    # ✅ Sanitize inputs
    title = html.escape(data["title"].strip())
    content = html.escape(data["content"].strip())
    category = data["category"].strip()
    ui_lang = data.get("lang", "en")

    # 🌐 Detect language
    try:
        original_lang = detect(f"{title} {content}")
    except Exception:
        original_lang = "und"

    # ⛔ Rate-limit OpenAI
    if not can_call_openai(limit=10):
        return jsonify({
            "error": "AI moderation temporarily unavailable. Too many requests this hour. Try again later.",
            "remaining_calls": 0
        }), 429

    # 🤖 Moderate content
    try:
        review_status = moderate_post(title, content)
    except Exception as e:
        print(f"❌ Moderation error: {e}")
        review_status = "needs_review"

    # 💾 Update post
    post.title = title
    post.content = content
    post.category = category
    post.updated = datetime.now()
    post.review_status = review_status
    post.original_lang = original_lang
    session.commit()

    # 🌍 Translate if needed
    if original_lang != "en":
        try:
            print(f"🌍 Translating updated post {post.id} from {original_lang} to English")
            title_en, content_en = translate_post(title, content, "en")
            save_translation(post.id, "en", title_en, content_en)
        except Exception as e:
            print(f"⚠️ Translation failed: {e}")

    # ✅ Build response
    response = {
        "post_id": post.id,
        "review_status": review_status
    }

    if review_status == "approved":
        response["message"] = "✅ Post updated and remains publicly visible."
    elif review_status == "needs_review":
        response["message"] = (
            "⚠️ Your updated post has been flagged for review. It is temporarily hidden from the public."
        )
    else:  # rejected
        response["message"] = (
            "🚫 Your post contains inappropriate or harmful language and has been rejected. "
            "It will not be visible to others. Please review our content guidelines."
        )

    if ui_lang != original_lang:
        response["warning"] = f"⚠️ The text appears to be in {original_lang}, not {ui_lang}."

    return jsonify(response), 200



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
def delete_post_v2(current_user, post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # 🛡️ Allow if user is author OR admin
    if post.user_id != current_user.id and not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    session.delete(post)
    session.commit()
    return jsonify({"message": "Post deleted"})


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
    lang = request.args.get("lang", "en")

    if not query:
        return jsonify({"error": "Missing query parameter `q`"}), 400

    posts = session.query(Post).options(
        joinedload(Post.user),
        joinedload(Post.translations)
    ).all()

    results = []

    for post in posts:
        author_match = query in (post.user.username or "").lower()

        # Defaults to original
        result_title = post.title
        result_content = post.content

        matched = False

        # First check translated version if not in original language
        if lang != "en":
            for t in post.translations:
                if t.lang == lang:
                    if query in (t.title or "").lower() or query in (t.content or "").lower():
                        result_title = t.title
                        result_content = t.content
                        matched = True
                        break

        # Check original if no match yet
        if not matched:
            if (
                query in (post.title or "").lower()
                or query in (post.content or "").lower()
                or author_match
            ):
                matched = True

        if matched:
            results.append({
                "id": post.id,
                "author": post.user.username,
                "title": result_title,
                "content": result_content,
                "category": post.category,
                "date": post.date.strftime("%B %d, %Y") if post.date else None,
                "updated": post.updated.strftime("%B %d, %Y") if post.updated else None,
                "likes": len(post.liked_by)
            })

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
@token_required
def like_post(current_user, post_id):
    try:
        post = session.query(Post).filter_by(id=post_id).first()
        if not post:
            return jsonify({"error": "Post not found"}), 404

        existing_like = session.query(PostLike).filter_by(user_id=current_user.id, post_id=post_id).first()
        if existing_like:
            session.delete(existing_like)
            liked_by_user = False
            message = f"👎 {current_user.username} unliked post {post_id}"
        else:
            new_like = PostLike(user_id=current_user.id, post_id=post_id)
            session.add(new_like)
            liked_by_user = True
            message = f"❤️ {current_user.username} liked post {post_id}"

        session.commit()
        print(message)

        # ✅ Notify post author (non-blocking)
        if (
                liked_by_user
                and post.user
                and post.user.email
                and post.user.notifications_enabled  # ✅ user wants notifications
                and post.user.id != current_user.id
        ):
            Thread(
                target=send_email,
                args=(
                    current_app._get_current_object(),
                    post.user.email,
                    "❤️ Someone liked your post",
                    f"{current_user.username} liked your post: {post.title}"
                )
            ).start()

        return jsonify({
            "message": message,
            "likes": len(post.liked_by),
            "liked_by_current_user": liked_by_user
        }), 200

    except Exception as e:
        print("❌ Error in like route:", e)
        return jsonify({"error": "Something went wrong"}), 500



@v2.route("/posts/<int:post_id>/comments", methods=["POST"])
@token_required
def add_comment_v2(current_user, post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "Comment text required"}), 400

    if not can_call_openai(limit=10):
        return jsonify({"error": "AI moderation limit reached. Try again later."}), 429

    # 🧠 AI moderation
    moderation_result = moderate_post("Comment", data["text"])

    if moderation_result == "rejected":
        return jsonify({"error": "Comment rejected due to harmful or inappropriate content."}), 403

    if moderation_result == "needs_review":
        return jsonify({"warning": "Comment submitted for review. It will be published after approval."}), 202

    # ✅ Save approved comment
    comment = Comment(
        post_id=post.id,
        author=current_user.username,
        text=data["text"],
        date=datetime.now()
    )

    session.add(comment)
    session.commit()

    # ✅ Notify post author (non-blocking)
    if (
            post.user
            and post.user.email
            and post.user.notifications_enabled  # ✅ user wants notifications
            and post.user.id != current_user.id
    ):
        Thread(
            target=send_email,
            args=(
                current_app._get_current_object(),
                post.user.email,
                "💬 New comment on your post",
                f"{current_user.username} commented on your post: {post.title}\n\n“{comment.text}”"
            )
        ).start()

    return jsonify({
        "message": "Comment added",
        "comment": {
            "id": comment.id,
            "author": comment.author,
            "text": comment.text,
            "date": comment.date.strftime("%B %d, %Y")
        }
    }), 201



@v2.route("/posts/<int:post_id>/comments", methods=["GET"])
@limiter.exempt
@v2.route("/posts/<int:post_id>/comments", methods=["GET"])
@limiter.exempt
def get_comments_v2(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comments = session.query(Comment).filter_by(post_id=post_id).all()
    comment_data = [
        {
            "id": c.id,
            "author": c.author,
            "text": c.text,
            "date": c.date.strftime("%B %d, %Y") if c.date else ""
        }
        for c in comments
    ]

    return jsonify({
        "comments": comment_data,
        "comment_count": len(comment_data)  # or use .count() if more efficient
    })




@v2.route("/comments/<int:comment_id>", methods=["DELETE"])
@token_required
def delete_comment(user, comment_id):
    comment = session.query(Comment).get(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    # Check if the user is the author or admin
    if comment.author != user.username and not user.is_admin:
        return jsonify({"error": "Unauthorized to delete this comment"}), 403

    session.delete(comment)
    session.commit()
    return jsonify({"message": f"Comment {comment_id} deleted"}), 200


# -------------------------
# POST /register
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
# POST /login
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


@v2.route("/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    return jsonify({
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin
    })

# -------------------------
# POST /login
# -------------------------

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


# -------------------------
# Admin Route for Viewing Usage
# -------------------------

@v2.route("/admin/openai-usage", methods=["GET"])
@token_required
@limiter.limit("3 per minute")
def view_openai_usage(current_user):
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    from utils import openai_usage_counter
    from collections import defaultdict
    import datetime

    usage_summary = defaultdict(lambda: defaultdict(int))  # username -> hour -> count

    for token, timestamps in openai_usage_counter.items():
        # Get user from token
        user = get_user_from_token_value(token)
        username = user.username if user else "unknown"

        for ts in timestamps:
            dt = datetime.datetime.fromtimestamp(ts)
            hour_key = dt.strftime("%Y-%m-%d %H:00")
            usage_summary[username][hour_key] += 1

    return jsonify(usage_summary)


@v2.route("/ai-usage", methods=["GET"])
def get_ai_usage_status():
    from utils import openai_usage_counter, can_call_openai
    remaining = max(0, 10 - sum(len(v) for v in openai_usage_counter.values()))
    return jsonify({"remaining_calls": remaining})


