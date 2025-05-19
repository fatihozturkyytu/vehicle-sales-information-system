import unittest
import sqlite3

DB_PATH = "test_users.db"

class TestSubmitOffer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
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
        """)
        # Temizle ve test verisi ekle
        c.execute("DELETE FROM customers WHERE name = 'Ali' AND surname = 'Yılmaz'")
        c.execute("""
            INSERT INTO customers (name, surname, interested_model, offer_requested, proposal_price)
            VALUES (?, ?, ?, ?, ?)
        """, ('Ali', 'Yılmaz', 'Civic', 1, None))
        conn.commit()
        conn.close()

    def test_proposal_price_update(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Müşteriyi ID üzerinden al
        c.execute("SELECT id FROM customers WHERE name = 'Ali' AND surname = 'Yılmaz'")
        customer_id = c.fetchone()[0]

        # Teklif güncelle
        new_price = 250000
        c.execute("UPDATE customers SET proposal_price = ? WHERE id = ?", (new_price, customer_id))
        conn.commit()

        # Kontrol
        c.execute("SELECT proposal_price FROM customers WHERE id = ?", (customer_id,))
        price = c.fetchone()[0]
        conn.close()

        self.assertEqual(price, new_price)

    @classmethod
    def tearDownClass(cls):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM customers WHERE name = 'Ali' AND surname = 'Yılmaz'")
        conn.commit()
        conn.close()

    #@classmethod
    #def tearDownClass(cls):
        # Test sonunda veritabanını sil
     #   if os.path.exists(DB_PATH):
      #      os.remove(DB_PATH)
if __name__ == "__main__":
    unittest.main()
