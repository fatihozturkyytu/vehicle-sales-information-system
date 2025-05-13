import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM vehicles WHERE brand = "BMW"
""")

conn.commit()
conn.close()