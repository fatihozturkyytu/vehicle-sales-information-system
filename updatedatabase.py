import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Add 'email' if it doesn't exist
try:
    cursor.execute("ALTER TABLE customers ADD COLUMN email TEXT")
except sqlite3.OperationalError:
    print("Column 'email' already exists.")

# Add 'phone' if it doesn't exist
try:
    cursor.execute("ALTER TABLE customers ADD COLUMN phone TEXT")
except sqlite3.OperationalError:
    print("Column 'phone' already exists.")

conn.commit()
conn.close()