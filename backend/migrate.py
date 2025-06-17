from sqlalchemy import create_engine, text

# Adjust to your actual DB path or URI
engine = create_engine("sqlite:///your_database_name.db")

with engine.connect() as conn:
    try:
        #conn.execute(text("ALTER TABLE posts ADD COLUMN original_lang TEXT DEFAULT 'en';"))
        print("✅ Column 'original_lang' added.")
    except Exception as e:
        print(f"⚠️ Could not alter table: {e}")