import sqlite3

# Always use the correct path to the backend database
conn = sqlite3.connect("backend/blog.db")
cursor = conn.cursor()

# Delete all translations with id >= 13
cursor.execute("DELETE FROM translations WHERE id >= 13;")
print("🗑️ Deleted translations with ID >= 13")

# Delete all posts with id >= 5
cursor.execute("DELETE FROM posts WHERE id >= 5;")
print("🗑️ Deleted posts with ID >= 5")

# Confirm remaining entries
cursor.execute("SELECT COUNT(*) FROM translations;")
print("✅ Remaining translations:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM posts;")
print("✅ Remaining posts:", cursor.fetchone()[0])

conn.commit()
conn.close()