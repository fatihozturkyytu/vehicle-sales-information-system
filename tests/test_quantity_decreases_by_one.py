import unittest
import sqlite3
import os
from types import SimpleNamespace

# test ortamında kullanılacak DB
TEST_DB = "test_users.db"

# Vehicle ve Stock sınıfı örnek olacak şekilde burada tanımlanıyor (gerçek ortamda import edilir)
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

class Stock:
    DB_PATH = TEST_DB

    def __init__(self, vehicle, year, color, price, quantity):
        self.vehicle = vehicle
        self.year = year
        self.color = color
        self.price = price
        self.quantity = quantity

    @classmethod
    def _update_db_quantity(cls, stock):
        with sqlite3.connect(cls.DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE stocks
                SET quantity = ?
                WHERE brand = ? AND model = ? AND year = ? AND color = ? AND price = ?
            """, (stock.quantity, stock.vehicle.brand, stock.vehicle.model, stock.year, stock.color, stock.price))
            conn.commit()

class TestStockQuantityUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        with sqlite3.connect(TEST_DB) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    color TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )
            ''')
            conn.commit()

        vehicle = Vehicle("test_brand", "test_model")
        cls.test_stock = Stock(vehicle, 2023, "Black", 100000, 5)

        with sqlite3.connect(TEST_DB) as conn:
            c = conn.cursor()
            c.execute("""INSERT INTO stocks (brand, model, year, color, price, quantity)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                      (vehicle.brand, vehicle.model, 2023, "Black", 100000, 5))
            conn.commit()

    def test_quantity_decreases_by_one(self):
        self.test_stock.quantity = 4
        Stock._update_db_quantity(self.test_stock)

        with sqlite3.connect(TEST_DB) as conn:
            c = conn.cursor()
            c.execute("""SELECT quantity FROM stocks
                         WHERE brand=? AND model=? AND year=? AND color=? AND price=?""",
                      (self.test_stock.vehicle.brand,
                       self.test_stock.vehicle.model,
                       self.test_stock.year,
                       self.test_stock.color,
                       self.test_stock.price))
            row = c.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], 4)


unittest.main(argv=[''], exit=False)
