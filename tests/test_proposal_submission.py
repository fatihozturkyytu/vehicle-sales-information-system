import unittest
import sqlite3

DB_PATH = "test_users.db"

class TestProposalSubmission(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Test müşterisi oluştur
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                interested_model TEXT NOT NULL,
                offer_requested INTEGER NOT NULL CHECK(offer_requested IN (0, 1)),
                proposal_price INTEGER
            )
        ''')
        c.execute("DELETE FROM customers WHERE name = 'Test' AND surname = 'User'")
        c.execute('''
            INSERT INTO customers (name, surname, interested_model, offer_requested, proposal_price)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Test", "User", "Honda Civic", 1, None))
        conn.commit()
        conn.close()

    def test_proposal_update(self):
        # Veri tabanında son eklenen test müşterisini çek
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM customers WHERE name = 'Test' AND surname = 'User'")
        customer_id = c.fetchone()[0]

        # Teklif ver: fiyat güncelle
        new_price = 150000
        c.execute("UPDATE customers SET proposal_price = ? WHERE id = ?", (new_price, customer_id))
        conn.commit()

        # Teklifin güncellenip güncellenmediğini kontrol et
        c.execute("SELECT proposal_price FROM customers WHERE id = ?", (customer_id,))
        updated_price = c.fetchone()[0]
        conn.close()

        self.assertEqual(updated_price, new_price)

    @classmethod
    def tearDownClass(cls):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM customers WHERE name = 'Test' AND surname = 'User'")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    unittest.main()
