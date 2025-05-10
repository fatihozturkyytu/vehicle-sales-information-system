import sqlite3
from datetime import datetime
from models.vehicle import Vehicle

DB_PATH = "users.db"  # Veritabanı yolu

class Showroom:
    @classmethod
    def init_db(cls):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(''' 
                CREATE TABLE IF NOT EXISTS showroom (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year TEXT NOT NULL,
                    color TEXT NOT NULL,
                    price TEXT NOT NULL,
                    purpose TEXT CHECK(purpose IN ('display', 'sales')) NOT NULL,
                    customer_name TEXT,
                    customer_surname TEXT,
                    sale_price REAL
                )
            ''')
            conn.commit()

    @classmethod
    def add_display_vehicle(cls, stock_item):
        cls._save_to_db(stock_item, "display")

    @classmethod
    def add_sales_vehicle(cls, stock_item, name, surname, price, delivered_at):
        """Satış için showroom'a araç ekler ve teslimat tarihiyle birlikte kaydeder"""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO showroom 
                         (brand, model, year, color, price, customer_name, customer_surname, purpose, sale_price)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (stock_item.vehicle.brand,
                       stock_item.vehicle.model,
                       stock_item.year,
                       stock_item.color,
                       price,
                       name,
                       surname,
                       "sales",  # Purpose is sales
                       price))  # Sale price
            conn.commit()

    @classmethod
    def _save_to_db(cls, stock_item, purpose):
        """Stock item'ını veritabanına kaydeder."""
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO showroom 
                         (brand, model, year, color, price, purpose) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (stock_item.vehicle.brand,
                       stock_item.vehicle.model,
                       stock_item.year,
                       stock_item.color,
                       stock_item.price,
                       purpose))
            conn.commit()

    @classmethod
    def get_display_vehicles(cls):
        """Display amaçlı showroom'daki araçları döndürür"""
        return cls._fetch_from_db("display")

    @classmethod
    def get_sales_vehicles(cls):
        """Sales amaçlı showroom'daki araçları döndürür"""
        return cls._fetch_from_db("sales")

    @classmethod
    def _fetch_from_db(cls, purpose):
        """Veritabanından showroom'daki araçları çeker ve formatlar."""
        result = []
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(""" 
                SELECT brand, model, year, color, price, customer_name, customer_surname, sale_price
                FROM showroom WHERE purpose = ?
            """, (purpose,))
            for row in c.fetchall():
                vehicle = Vehicle(row[0], row[1])
                fake_stock = type("FakeStock", (), {})()
                fake_stock.vehicle = vehicle
                fake_stock.year = row[2]
                fake_stock.color = row[3]
                fake_stock.price = row[4]
                fake_stock.customer_name = row[5]
                fake_stock.customer_surname = row[6]
                fake_stock.sale_price = row[7]
                fake_stock.to_showroom_string = lambda self=fake_stock: (
                    f"{self.vehicle} - {self.year} - {self.color} - {self.price}₺"
                    if purpose == "display"
                    else f"{self.vehicle} - {self.year} - {self.color} - {self.sale_price}₺ | Müşteri: {self.customer_name} {self.customer_surname}"
                )
                result.append(fake_stock)
        return result
