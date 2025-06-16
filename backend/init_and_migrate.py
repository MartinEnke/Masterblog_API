import json
from datetime import datetime
from werkzeug.security import generate_password_hash

from db import Base, engine, session
from models import User, Post, Comment

# Step 1: Create all tables
Base.metadata.create_all(engine)

# Step 2: Migrate users
def migrate_users(path="user.json"):
    with open(path, "r") as f:
        users = json.load(f)

    for username, password in users.items():
        if not session.query(User).filter_by(username=username).first():
            hashed_pw = generate_password_hash(password)
            session.add(User(username=username, password=hashed_pw))
            print(f"✅ Added user: {username}")
    session.commit()

# Step 3: Migrate posts
def migrate_posts(path="blog_posts.json"):
    with open(path, "r") as f:
        posts = json.load(f)

    for p in posts:
        user = session.query(User).filter_by(username=p["author"]).first()
        if not user:
            print(f"⚠️ Skipping post — unknown author: {p['author']}")
            continue

        if session.query(Post).filter_by(id=p["id"]).first():
            continue

        new_post = Post(
            id=p["id"],
            user_id=user.id,
            title=p["title"],
            content=p["content"],
            category=p["category"],
            date=datetime.strptime(p["date"], "%B %d, %Y") if p.get("date") else None,
            updated=datetime.strptime(p["updated"], "%B %d, %Y") if p.get("updated") else None,
            likes=p.get("likes", 0)
        )
        session.add(new_post)
        session.flush()

        for c in p.get("comments", []):
            comment = Comment(
                post_id=new_post.id,
                author=c["author"],
                text=c["text"],
                date=datetime.strptime(c["date"], "%B %d, %Y") if c.get("date") else None
            )
            session.add(comment)

    session.commit()
    print("✅ Posts and comments migrated.")

# Run it all
if __name__ == "__main__":
    migrate_users()
    migrate_posts()
