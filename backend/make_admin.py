from backend.db import session
from backend.models import User
from dotenv import load_dotenv


load_dotenv()

def make_admin(username="admin"):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print(f"❌ User '{username}' not found")
        return

    user.is_admin = True
    session.commit()
    print(f"✅ User '{username}' is now an admin")

if __name__ == "__main__":
    make_admin()