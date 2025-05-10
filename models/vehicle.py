# models/vehicle.py
import sqlite3

DB_PATH = "users.db"

class Vehicle:
    vehicle_list = []

    def __init__(self, brand, model):
        self.brand = brand.strip()
        self.model = model.strip()

    def __str__(self):
        return f"{self.brand} {self.model}"

    @classmethod
    def init_db(cls):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT NOT NULL,
                    model TEXT NOT NULL
                )
            ''')
            conn.commit()

    @classmethod
    def add(cls, brand, model):
        if not brand or not model:
            return None, "Marka ve model boş olamaz."

        vehicle = cls(brand, model)
        cls.vehicle_list.append(vehicle)

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO vehicles (brand, model) VALUES (?, ?)", (vehicle.brand, vehicle.model))
            conn.commit()

        return vehicle, None

    @classmethod
    def get_all(cls):
        cls.vehicle_list.clear()
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT brand, model FROM vehicles")
            for row in c.fetchall():
                cls.vehicle_list.append(cls(row[0], row[1]))
        return cls.vehicle_list

    @classmethod
    def get_by_index(cls, index):
        try:
            return cls.vehicle_list[index], None
        except IndexError:
            return None, "Model seçilmedi."

    @classmethod
    def search(cls, query):
        query = query.lower().strip()
        return [v for v in cls.get_all() if query in str(v).lower()]