import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

import json
from datetime import datetime
from werkzeug.security import generate_password_hash

# Import from backend
from db import Base, engine, session
from models import User, Post, Comment

# Reset DB
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Load users
with open("backend/user.json") as f:
    users_data = json.load(f)

users = {}
for username, password in users_data.items():
    hashed_pw = generate_password_hash(password)
    user = User(username=username, password=hashed_pw)
    session.add(user)
    users[username] = user

session.commit()

# Load posts
with open("backend/blog_posts.json") as f:
    posts_data = json.load(f)

for post_data in posts_data:
    user = users.get(post_data["author"])
    if not user:
        continue

    date = datetime.strptime(post_data["date"], "%B %d, %Y")
    updated = datetime.strptime(post_data["updated"], "%B %d, %Y") if post_data["updated"] else None

    post = Post(
        user_id=user.id,
        title=post_data["title"],
        content=post_data["content"],
        category=post_data["category"],
        date=date,
        updated=updated,
        review_status="approved"  # ✅ New line
    )
    session.add(post)
    session.flush()

    # If you still include comments
    for comment_data in post_data.get("comments", []):
        comment_date = datetime.strptime(comment_data["date"], "%B %d, %Y")
        comment = Comment(
            post_id=post.id,
            author=comment_data["author"],
            text=comment_data["text"],
            date=comment_date,
        )
        session.add(comment)

session.commit()
print("✅ Database populated successfully!")
