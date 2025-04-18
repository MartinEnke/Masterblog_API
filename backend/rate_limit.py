# rate_limit.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request

def get_token_or_ip():
    return request.headers.get("Authorization") or get_remote_address()

limiter = Limiter(
    key_func=get_token_or_ip,         # avoids blocking of users sharing an IP-address (f.e. in Cafés)
    default_limits=["100 per hour"]   # if logged in - token is used, logged out - ip is used
)