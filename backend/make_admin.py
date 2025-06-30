from backend.db import session
from backend.models import User

admin_user = session.query(User).filter_by(username="admin").first()
admin_user.is_admin = True
session.commit()