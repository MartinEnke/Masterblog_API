from flask import jsonify
import os
import json
from models import Post, Comment
from translations_db import session
from datetime import datetime


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
    """Load all blog posts from the database as dicts."""
    posts = session.query(Post).all()
    result = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "author": post.author.username if post.author else "Unknown",
            "title": post.title,
            "content": post.content,
            "category": post.category,
            "date": post.date.strftime("%B %d, %Y") if post.date else None,
            "updated": post.updated.strftime("%B %d, %Y") if post.updated else None,
            "likes": post.likes,
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

