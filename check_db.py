import os
import sqlite3

BASE_DIR = os.path.join(os.path.dirname(__file__))
DB_NAME = os.path.join(BASE_DIR, "../mobile_shop.db")

print("CHECKING:", DB_NAME)

conn = sqlite3.connect(DB_NAME)

cur = conn.cursor()

cur.execute("PRAGMA table_info(sales)")

for row in cur.fetchall():
    print(row)

conn.close()