import unittest
import sqlite3

DB_PATH = "test_users.db"

class TestTestDriveApproval(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB_PATH)
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                interested_model TEXT NOT NULL,
                offer_requested INTEGER NOT NULL CHECK(offer_requested IN (0, 1)),
                proposal_price INTEGER,
                test_drive_requested INTEGER DEFAULT 0,
                test_drive_approved INTEGER,
                email TEXT,
                phone TEXT
            )
        ''')
        cls.cursor.execute("DELETE FROM customers WHERE name = 'test_user_drive'")
        cls.cursor.execute("""
            INSERT INTO customers (name, surname, interested_model, offer_requested, test_drive_requested)
            VALUES (?, ?, ?, ?, ?)""", ('test_user_drive', 'drive_test', 'model_x', 0, 1))
        cls.conn.commit()

    def test_approve_test_drive(self):
        # test_drive_approved'ı 1 yap
        self.cursor.execute("""
            UPDATE customers
            SET test_drive_approved = 1
            WHERE name = 'test_user_drive'
        """)
        self.conn.commit()

        # kontrol
        self.cursor.execute("""
            SELECT test_drive_approved FROM customers
            WHERE name = 'test_user_drive'
        """)
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 1)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("DELETE FROM customers WHERE name = 'test_user_drive'")
        cls.conn.commit()
        cls.conn.close()

if __name__ == "__main__":
    unittest.main()
