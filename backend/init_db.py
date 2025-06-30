# backend/init_db.py

from backend.db import Base, engine, session
from backend.models import User, Post, Comment, PostLike
from backend.translations_db import PostTranslation

from datetime import datetime

def init_database():
    print("📦 Creating all tables...")
    Base.metadata.create_all(engine)
    print("✅ Tables created.")

    # Optionally seed a test user and post (skip if you don't want demo data)
    if not session.query(User).first():
        user = User(username="demo", password="demo123", email="demo@example.com")
        session.add(user)
        session.commit()

        post = Post(
            user_id=user.id,
            title="Welcome to The Quiet Almanac",
            content="This is your first post. Edit or delete it as needed.",
            category="General",
            date=datetime.utcnow(),
            original_lang="en",
            review_status="approved"
        )
        session.add(post)
        session.commit()

        print("✅ Added demo user and post.")

if __name__ == "__main__":
    init_database()
