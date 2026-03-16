from backend.models import Post, Comment, PostLike
from backend.translations_db import session
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import os
from flask import request, current_app
from flask_limiter.util import get_remote_address
import re
import smtplib
from email.mime.text import MIMEText

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def validate_post_data(data):
    """
    Validate post data fields for title, content, and category.

    Args:
        data (dict): Post data containing 'title', 'content', and 'category'.

    Returns:
        dict or None: Returns error dict if validation fails, else None.
    """
    if not data:
        return {"error": "Enter a title, content, and category"}

    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    category = data.get("category", "").strip()

    if not (3 <= len(title) <= 100):
        return {"error": "Title must be 3–150 characters"}
    if not (10 <= len(content) <= 2000):
        return {"error": "Content must be 10–2000 characters"}
    if not re.match(r"^[\w\s\-]{1,50}$", category):
        return {"error": "Invalid category (only letters, numbers, dashes allowed)"}

    return None


def load_posts():
    """
    Load all posts from the database with dynamic like counts and comments.

    Returns:
        list of dict: List of posts with keys like id, author, title, content,
                      category, date, updated, likes, and comments.
    """
    posts = session.query(Post).all()
    result = []

    for post in posts:
        like_count = session.query(PostLike).filter_by(post_id=post.id).count()

        post_dict = {
            "id": post.id,
            "author": post.author.username if post.author else "Unknown",
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "date": post.date.strftime("%B %d, %Y") if post.date else None,
            "updated": post.updated.strftime("%B %d, %Y") if post.updated else None,
            "likes": like_count,
            "comments": [
                {
                    "author": c.author,
                    "text": c.text,
                    "date": c.date.strftime("%B %d, %Y") if c.date else None
                }
                for c in post.comments
            ]
        }

        result.append(post_dict)

    return result


def save_post(post_data):
    """
    Save a new post to the database.

    Args:
        post_data (dict): Dictionary with post data including 'author',
                          'title', 'content', 'category', and optional 'likes'.

    Returns:
        int: ID of the newly created post.
    """
    post = Post(
        author=post_data["author"],
        title=post_data["title"],
        content=post_data["content"],
        category=post_data["category"],
        likes=post_data.get("likes", 0)
    )
    session.add(post)
    session.commit()
    return post.id


def delete_post_db(post_id, current_user):
    """
    Delete a post if it exists and the current user is the author.

    Args:
        post_id (int): ID of the post to delete.
        current_user (User): User requesting deletion.

    Returns:
        tuple: JSON response dict and HTTP status code.
    """
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return {"error": f"Post with ID {post_id} not found"}, 404

    if post.author != current_user:
        return {"error": "Unauthorized to delete this post"}, 403

    session.delete(post)
    session.commit()
    return {"message": f"Post {post_id} deleted"}, 200


def update_post_db(post_id, data):
    """
    Update the title, content, category, and updated timestamp of a post.

    Args:
        post_id (int): ID of the post to update.
        data (dict): Dictionary containing 'title', 'content', and 'category'.

    Returns:
        Post or None: Updated Post object if found, else None.
    """
    post = session.query(Post).filter_by(id=post_id).first()
    if post:
        post.title = data["title"]
        post.content = data["content"]
        post.category = data["category"]
        post.updated = datetime.utcnow()
        session.commit()
        return post
    return None


def like_post_db(post_id):
    """
    Increment the like count of a post.

    Args:
        post_id (int): ID of the post to like.

    Returns:
        tuple: JSON response dict and HTTP status code.
    """
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return {"error": f"Post with ID {post_id} not found"}, 404

    post.likes = (post.likes or 0) + 1
    session.commit()
    return {"message": f"Post {post_id} liked", "likes": post.likes}, 200


def send_email(app, to_email, subject, body):
    """
    Send an email using SMTP or print to console in development mode.

    Args:
        app (Flask): Flask application context.
        to_email (str): Recipient email address.
        subject (str): Email subject.
        body (str): Email body content.

    Returns:
        None
    """
    with app.app_context():
        if current_app.config.get("ENV") == "development":
            print(f"📧 Dev mode: would send email to {to_email}:\nSubject: {subject}\n{body}")
            return

        smtp_server = current_app.config["SMTP_SERVER"]
        smtp_port = current_app.config["SMTP_PORT"]
        smtp_ssl_port = current_app.config.get("SMTP_SSL_PORT", 465)
        smtp_user = current_app.config["SMTP_USERNAME"]
        smtp_password = current_app.config["SMTP_PASSWORD"]
        from_email = current_app.config.get("EMAIL_FROM", smtp_user)

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, [to_email], msg.as_string())
            server.quit()
            print(f"✅ Email sent to {to_email} via STARTTLS")

        except Exception as e1:
            print(f"⚠️ STARTTLS failed: {e1}. Trying SSL fallback...")

            try:
                server = smtplib.SMTP_SSL(smtp_server, smtp_ssl_port)
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email], msg.as_string())
                server.quit()
                print(f"✅ Email sent to {to_email} via SMTP_SSL")

            except Exception as e2:
                print(f"❌ Failed to send email to {to_email}: {e2}")


def moderate_post(title, content):
    """
    Use Gemini to moderate post content.

    Args:
        title (str): Post title.
        content (str): Post content.

    Returns:
        str: One of 'approved', 'rejected', or 'needs_review'.
    """
    prompt = (
        "You are a helpful but balanced content moderator.\n"
        "Return ONLY one of: approved, rejected, or needs_review.\n"
        "rejected = clearly offensive, harmful, violent, or unsafe\n"
        "needs_review = likely problematic but unclear — use this rarely\n"
        "approved = appropriate or benign\n"
        "Be generous with what is safe. Avoid flagging harmless or emotional expressions.\n\n"
        f"Title:\n{title}\n\nContent:\n{content}"
    )

    try:
        print("🔍 Prompt being sent to Gemini:\n", prompt)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        decision = (response.text or "").strip().lower()
        print("🤖 Moderation decision:", decision)

        if decision in ["approved", "rejected", "needs_review"]:
            return decision

        print("⚠️ Unexpected moderation result:", decision)
        return "needs_review"

    except Exception as e:
        print(f"❌ Moderation check failed: {e}")
        return "needs_review"


gemini_usage_counter = {}


def get_request_identity():
    """
    Get a unique identifier for the requestor based on Authorization header
    or IP address.

    Returns:
        str: Identifier string.
    """
    return request.headers.get("Authorization", "anonymous") or get_remote_address()


def can_call_gemini(limit=10):
    """
    Rate limit Gemini API calls to a maximum number per hour per user/IP.

    Args:
        limit (int): Maximum allowed calls per hour.

    Returns:
        bool: True if call is allowed, False if limit exceeded.
    """
    from time import time

    identity = get_request_identity()
    now = time()

    if identity not in gemini_usage_counter:
        gemini_usage_counter[identity] = []

    gemini_usage_counter[identity] = [
        t for t in gemini_usage_counter[identity] if now - t < 3600
    ]

    if len(gemini_usage_counter[identity]) >= limit:
        return False

    gemini_usage_counter[identity].append(now)
    return True