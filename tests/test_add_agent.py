import unittest
import sqlite3
import os

TEST_DB = "test_users.db"

class TestDuplicateAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        # Eğer varsa sil ve yeniden ekle
        #teardownclass oldugu icin aslinda buna gerek kalmayabilir..
        c.execute("DELETE FROM users WHERE id = 'duplicate_agent'")
        c.execute("INSERT INTO users (id, password, role) VALUES (?, ?, ?)", ('duplicate_agent', '123456', 'agent'))
        conn.commit()
        conn.close()

    def test_duplicate_entry_should_fail(self):
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO users (id, password, role) VALUES (?, ?, ?)", ('duplicate_agent', 'anotherpw', 'agent'))
        conn.close()

 #   @classmethod
  #  def tearDownClass(cls):
   #     if os.path.exists(TEST_DB):
    #        os.remove(TEST_DB)

if __name__ == "__main__":
    unittest.main()
