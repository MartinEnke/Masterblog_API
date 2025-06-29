from flask import jsonify
from models import Post, Comment, PostLike
from translations_db import session
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import os
from flask import request
from flask_limiter.util import get_remote_address
import re
load_dotenv()
import smtplib
from email.mime.text import MIMEText
from flask import current_app

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def validate_post_data(data):
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
    """Load all blog posts from the database as dicts, including dynamic like counts."""
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
            "likes": like_count,  # ✅ dynamically computed like count
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
    """Add a new post to the database."""
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
    """Delete a post from the database if the current user is the author."""
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return {"error": f"Post with ID {post_id} not found"}, 404

    if post.author != current_user:
        return {"error": "Unauthorized to delete this post"}, 403

    session.delete(post)
    session.commit()
    return {"message": f"Post {post_id} deleted"}, 200


def update_post_db(post_id, data):
    post = session.query(Post).filter_by(id=post_id).first()
    if post:
        post.title = data['title']
        post.content = data['content']
        post.category = data['category']
        post.updated = datetime.utcnow()
        session.commit()
        return post
    return None


def like_post_db(post_id):
    """Increment the like count of a post in the database."""
    post = session.query(Post).filter_by(id=post_id).first()
    if not post:
        return {"error": f"Post with ID {post_id} not found"}, 404

    post.likes = (post.likes or 0) + 1
    session.commit()
    return {"message": f"Post {post_id} liked", "likes": post.likes}, 200


def send_email(app, to_email, subject, body):
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
            # Try STARTTLS first (most common for port 587)
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
                # Fallback: SSL (commonly used with port 465)
                server = smtplib.SMTP_SSL(smtp_server, smtp_ssl_port)
                server.login(smtp_user, smtp_password)
                server.sendmail(from_email, [to_email], msg.as_string())
                server.quit()
                print(f"✅ Email sent to {to_email} via SMTP_SSL")

            except Exception as e2:
                print(f"❌ Failed to send email to {to_email}: {e2}")


def moderate_post(title, content):
    """Moderate a post using gpt-4o-mini (educational-tier access)."""
    prompt = (
        '''You are a helpful but balanced content moderator.
           Return ONLY one of: 'approved', 'rejected', or 'needs_review'.
           'rejected' = clearly offensive, harmful, violent, or unsafe
           'needs_review' = likely problematic but unclear — use this rarely
           'approved' = appropriate or benign
           Be generous with what is safe. Avoid flagging harmless or emotional expressions.'''
           f"Title:\n{title}\n\nContent:\n{content}"
    )

    try:
        print("🔍 Prompt being sent to GPT:\n", prompt)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        decision = response.choices[0].message.content.strip().lower()
        print("🤖 Moderation decision:", decision)

        if decision in ["approved", "rejected", "needs_review"]:
            return decision

        print("⚠️ Unexpected moderation result:", decision)
        return "needs_review"

    except Exception as e:
        print(f"❌ Moderation check failed: {e}")
        return "needs_review"


openai_usage_counter = {}

def get_request_identity():
    return request.headers.get("Authorization", "anonymous") or get_remote_address()

def can_call_openai(limit=10):
    """Allow only `limit` requests per hour per user/IP"""
    from time import time
    identity = get_request_identity()
    now = time()

    if identity not in openai_usage_counter:
        openai_usage_counter[identity] = []

    # Keep only timestamps within the last hour
    openai_usage_counter[identity] = [
        t for t in openai_usage_counter[identity] if now - t < 3600
    ]

    if len(openai_usage_counter[identity]) >= limit:
        return False

    openai_usage_counter[identity].append(now)
    return True