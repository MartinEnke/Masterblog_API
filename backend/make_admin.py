from db import session
from models import User

admin_user = session.query(User).filter_by(username="admin").first()
admin_user.is_admin = True
session.commit()