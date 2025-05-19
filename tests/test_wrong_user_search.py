import unittest
import sqlite3
import os
DB_PATH = "test_users.db"

class TestFailSimulation(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        # Önce veriyi temizleyelim
        self.c.execute("DELETE FROM users WHERE id = 'agent123'")
        self.c.execute("INSERT INTO users (id, password, role) VALUES (?, ?, ?)", ('agent123', '123', 'agent'))
        self.conn.commit()

    def test_wrong_user_should_fail(self):
        # BURADA BİLEREK YANLIŞ ID'Yİ KONTROL EDİYORUZ
        self.c.execute("SELECT * FROM users WHERE id = 'wrong_id'")
        result = self.c.fetchone()
        # Burada aslında None dönecek ama biz var sanıyoruz
        self.assertIsNotNone(result)  # 🔴 Bu satır testin FAIL olmasını sağlar

    def tearDown(self):
        self.c.execute("DELETE FROM users WHERE id = 'agent123'")
        self.conn.commit()
        self.conn.close()

 #   @classmethod
  #  def tearDownClass(cls):
   #     # Test sonunda veritabanını sil
    #    if os.path.exists(DB_PATH):
     #       os.remove(DB_PATH)
if __name__ == "__main__":
    unittest.main()
