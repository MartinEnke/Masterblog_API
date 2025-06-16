import json
from datetime import datetime
from db import Base, session, engine
from models import User, Comment, Post

# ✅ Ensure tables exist
Base.metadata.create_all(engine)

def migrate_json_to_db():
    with open("blog_posts.json", "r") as f:
        posts_data = json.load(f)

    for p in posts_data:
        # Find the matching user
        user = session.query(User).filter_by(username=p["author"]).first()
        if not user:
            print(f"❌ Skipping post with unknown author: {p['author']}")
            continue

        new_post = Post(
            id=p["id"],
            author_id=user.id,
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

if __name__ == "__main__":
    migrate_json_to_db()
