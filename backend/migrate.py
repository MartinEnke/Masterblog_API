from sqlalchemy import create_engine, text

# Adjust this to your actual SQLite database path
engine = create_engine("sqlite:///blog.db")

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE posts ADD COLUMN original_lang TEXT DEFAULT 'en';"))
        print("✅ Column 'original_lang' added to posts.")
    except Exception as e:
        print(f"⚠️ Skipped adding 'original_lang' to posts: {e}")

    try:
        conn.execute(text("ALTER TABLE post_translations ADD COLUMN is_ai_translation BOOLEAN DEFAULT 0;"))
        print("✅ Column 'is_ai_translation' added to post_translations.")
    except Exception as e:
        print(f"⚠️ Skipped adding 'is_ai_translation' to post_translations: {e}")

    try:
        conn.execute(text("ALTER TABLE post_translations ADD COLUMN original_post_id INTEGER REFERENCES posts(id);"))
        print("✅ Column 'original_post_id' added to post_translations.")
    except Exception as e:
        print(f"⚠️ Skipped adding 'original_post_id' to post_translations: {e}")
