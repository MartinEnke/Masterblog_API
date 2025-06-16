import json
from db import Base, engine, session
from models import User
from werkzeug.security import generate_password_hash

# ✅ Make sure all tables exist before querying
Base.metadata.create_all(engine)

def migrate_users_from_json(json_path="user.json"):
    with open(json_path, "r") as f:
        user_data = json.load(f)

    for username, password in user_data.items():
        existing_user = session.query(User).filter_by(username=username).first()
        if not existing_user:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            session.add(new_user)
            print(f"✅ Added user: {username}")
        else:
            print(f"⚠️ User already exists: {username}")

    session.commit()
    print("✅ User migration complete.")

if __name__ == "__main__":
    migrate_users_from_json()
