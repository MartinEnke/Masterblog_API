# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from db import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username})>"

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime)
    likes = Column(Integer, default=0)

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    @property
    def author(self):
        return self.user.username

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    author = Column(String, default="Anonymous")
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
