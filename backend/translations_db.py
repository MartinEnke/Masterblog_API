# translations_db.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base
from db import Base, engine, session

class PostTranslation(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, nullable=False)
    lang = Column(String(10), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('post_id', 'lang', name='uix_post_lang'),)

def init_db():
    Base.metadata.create_all(engine)

# Translation helpers
def get_translation(post_id, lang):
    return session.query(PostTranslation).filter_by(post_id=post_id, lang=lang).first()

def save_translation(post_id, lang, title, content):
    existing = get_translation(post_id, lang)
    if existing:
        existing.title = title
        existing.content = content
    else:
        new = PostTranslation(post_id=post_id, lang=lang, title=title, content=content)
        session.add(new)
    session.commit()
