
import sqlite3

conn = sqlite3.connect("mobile_shop.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(services)")

for row in cur.fetchall():
    print(row)

conn.close()