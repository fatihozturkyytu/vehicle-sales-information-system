from tkinter import messagebox
import sqlite3
from models.vehicle import Vehicle

DB_PATH = "users.db"

class Stock:
    stock_list = []

    def __init__(self, vehicle, year, color, price, quantity):
        self.vehicle = vehicle  # Vehicle object
        self.year = year
        self.color = color.strip()
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.vehicle} - {self.year} - {self.color} - {self.price}₺ - Adet: {self.quantity}"

    def matches(self, year, color):
        return self.year == year and self.color.lower() == color.lower()

    @classmethod
    def init_db(cls):
        with sqlite3.connect(DB_PATH) as conn:
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

    @classmethod
    def add(cls, vehicle, year, color, price, quantity):
        if not all([vehicle, year, color, price, quantity]):
            return None, "Tüm alanlar doldurulmalıdır."

        try:
            year = int(year)
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            return None, "Yıl, fiyat ve adet sayısal olmalıdır."

        stock = cls(vehicle, year, color, price, quantity)
        cls.stock_list.append(stock)

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO stocks (brand, model, year, color, price, quantity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (vehicle.brand, vehicle.model, year, color, price, quantity))
            conn.commit()

        return stock, None

    @classmethod
    def add_or_prompt_update(cls, vehicle, year, color, price, quantity):
        try:
            year = int(year)
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            return None, "Yıl, fiyat ve adet sayısal olmalıdır."

        for stock in cls.filter_by_vehicle(vehicle):
            if stock.matches(year, color):
                if stock.price == price:
                    stock.quantity += quantity
                    cls._update_db_quantity(stock)
                    return stock, None
                else:
                    result = messagebox.askyesno(
                        "Fiyat Farkı Var",
                        f"Aynı renk ve yılda stok daha önce {stock.price}₺ olarak eklenmiş.\n"
                        f"Yeni fiyat {price}₺.\n"
                        f"Fiyatı güncelleyip stoğa {quantity} adet eklemek ister misiniz?"
                    )
                    if result:
                        stock.price = price
                        stock.quantity += quantity
                        cls._update_db_price_and_quantity(stock)
                        return stock, None
                    else:
                        break
        return cls.add(vehicle, year, color, price, quantity)

    @classmethod
    def _update_db_quantity(cls, stock):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE stocks
                SET quantity = ?
                WHERE brand = ? AND model = ? AND year = ? AND color = ? AND price = ?
            """, (stock.quantity, stock.vehicle.brand, stock.vehicle.model, stock.year, stock.color, stock.price))
            conn.commit()

    @classmethod
    def _update_db_price_and_quantity(cls, stock):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE stocks
                SET price = ?, quantity = ?
                WHERE brand = ? AND model = ? AND year = ? AND color = ?
            """, (stock.price, stock.quantity, stock.vehicle.brand, stock.vehicle.model, stock.year, stock.color))
            conn.commit()

    @classmethod
    def filter_by_vehicle(cls, vehicle):
        cls.stock_list.clear()
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT brand, model, year, color, price, quantity FROM stocks
                WHERE brand = ? AND model = ?
            """, (vehicle.brand, vehicle.model))
            for row in c.fetchall():
                v = Vehicle(row[0], row[1])
                cls.stock_list.append(cls(v, row[2], row[3], row[4], row[5]))
        return cls.stock_list

    @classmethod
    def get_all(cls):
        cls.stock_list.clear()
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT brand, model, year, color, price, quantity FROM stocks")
            for row in c.fetchall():
                v = Vehicle(row[0], row[1])
                cls.stock_list.append(cls(v, row[2], row[3], row[4], row[5]))
        return cls.stock_list