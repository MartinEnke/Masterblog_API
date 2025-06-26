import sqlite3

# Always use the correct path to the backend database
conn = sqlite3.connect("backend/blog.db")
cursor = conn.cursor()

# # Delete all translations with id >= 13
# cursor.execute("UPDATE users SET email = NULL WHERE username = 'frank';")
#
# cursor.execute("UPDATE users SET email = 'trickform.info@gmail.com' WHERE username = 'martin';")
# print("🗑️ Deleted translations with ID >= 0")

# Delete all posts with id >= 5
cursor.execute("UPDATE users SET tts_demo_used = 0;")
print("🗑️ Deleted posts with ID >= 5")
#
# # Confirm remaining entries
# cursor.execute("SELECT COUNT(*) FROM translations;")
# print("✅ Remaining translations:", cursor.fetchone()[0])
#
# cursor.execute("SELECT COUNT(*) FROM posts;")
# print("✅ Remaining posts:", cursor.fetchone()[0])

conn.commit()
conn.close()