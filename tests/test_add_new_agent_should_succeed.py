import unittest
import sqlite3
import os

DB_PATH = "test_users.db"

class TestAddNewAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Veritabanı dosyasını oluştur (varsa temizle)
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def test_add_new_agent_should_succeed(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        new_id = "new_agent_01"
        password = "pass123"
        role = "agent"

        # Yeni kullanıcıyı ekle
        c.execute("INSERT INTO users (id, password, role) VALUES (?, ?, ?)", (new_id, password, role))
        conn.commit()

        # Doğrula: gerçekten eklenmiş mi?
        c.execute("SELECT * FROM users WHERE id = ?", (new_id,))
        user = c.fetchone()

        conn.close()

        self.assertIsNotNone(user)
        self.assertEqual(user[0], new_id)
        self.assertEqual(user[1], password)
        self.assertEqual(user[2], role)

 #   @classmethod
  #  def tearDownClass(cls):
   #     # Test sonunda veritabanını sil
    #    if os.path.exists(DB_PATH):
     #       os.remove(DB_PATH)

if __name__ == "__main__":
    unittest.main()
