import sqlite3

conn = sqlite3.connect("mobile_shop.db")
cur = conn.cursor()

cur.execute("DELETE FROM users")

conn.commit()
conn.close()

print("Users Deleted")
from modules.login import create_user

print(create_user("admin", "admin123", "Admin"))