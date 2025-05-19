import unittest
import sqlite3
import os
from types import SimpleNamespace

TEST_DB = "test_users.db"

class TestSoldVehicleEntry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # DB varsa sil
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        # Yeni veritabanı oluştur
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE sold_vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year TEXT NOT NULL,
                color TEXT NOT NULL,
                price TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                customer_surname TEXT NOT NULL,
                sold_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def test_sold_vehicle_inserts_correctly(self):
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()

        data = ("BMW", "320i", "2022", "Black", "750000", "Ali", "Yılmaz", "2025-05-20")
        c.execute('''
            INSERT INTO sold_vehicles (brand, model, year, color, price, customer_name, customer_surname, sold_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        conn.commit()

        # Kontrol
        c.execute("SELECT * FROM sold_vehicles WHERE brand='BMW' AND model='320i'")
        result = c.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[1:], data)  # id hariç tüm alanlar


if __name__ == "__main__":
    unittest.main()
