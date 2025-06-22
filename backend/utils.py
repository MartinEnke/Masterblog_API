from flask import jsonify
from models import Post, Comment, PostLike
from translations_db import session
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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