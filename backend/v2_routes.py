# -------------------------------
# 📦 Version 2 API – Main Entry
# -------------------------------
# In real projects, this might live in a separate file like v2_routes.py and be registered with a Blueprint.
# For now, we keep it inline to help demonstrate the structure and evolution.
from flask import Blueprint, jsonify, request
from datetime import datetime

v2 = Blueprint('v2', __name__, url_prefix='/api/v2')

# Dummy data source for now (reuse actual methods in real app)
def load_posts():
    return []

@v2.route('/posts', methods=['GET'])
def get_posts_v2():
    '''
    🆕 Version 2: Improved GET posts route.
    - Could support additional filters, fields, or formatting.
    - Clean separation from v1 ensures backwards compatibility.
    '''
    return jsonify({"message": "GET /posts in v2 – add improved logic here."})

@v2.route('/posts', methods=['POST'])
def add_post_v2():
    '''
    🆕 Version 2: Create a post with enhanced validation or tagging.
    '''
    data = request.get_json()
    return jsonify({"message": "POST /posts in v2 – new post created.", "data": data}), 201

@v2.route('/stats', methods=['GET'])
def get_stats_v2():
    '''
    🧮 Optional: v2-only stats route (could also exist in v1).
    '''
    return jsonify({"total_users": 42, "total_posts": 1337})
