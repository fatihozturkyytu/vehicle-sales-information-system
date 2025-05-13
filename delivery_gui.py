import tkinter as tk
import sqlite3
from tkinter import messagebox, simpledialog
from datetime import datetime

DB_PATH = "users.db"

def deliver_sold_vehicle(root):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, brand, model, year, color, price, customer_name, customer_surname FROM showroom WHERE purpose='sales'")
    vehicles = c.fetchall()

    if not vehicles:
        messagebox.showinfo("Bilgi", "Teslim edilecek satış amaçlı araç bulunamadı.")
        conn.close()
        return

    window = tk.Toplevel(root)
    window.title("Teslim Edilecek Araç Seç")
    window.geometry("600x400")

    def submit(index):
        selected = vehicles[index]

        # Teslimat tarihi
        delivered_at = simpledialog.askstring("Teslimat Tarihi", "Teslimat tarihini (YYYY-MM-DD) girin:")
        if not delivered_at:
            messagebox.showerror("Hata", "Teslimat tarihi girilmelidir.")
            return

        try:
            # Tarih formatını kontrol et
            datetime.strptime(delivered_at, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tarih formatı. Lütfen 'YYYY-MM-DD' formatında girin.")
            return

        # Müşteri adı ve soyadı, zaten araç ve stok yönetiminden geliyor
        customer_name = selected[6]
        customer_surname = selected[7]

        # Veritabanına ekle
        c.execute("""INSERT INTO sold_vehicles (brand, model, year, color, price, customer_name, customer_surname, sold_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (selected[1], selected[2], selected[3], selected[4], selected[5], customer_name, customer_surname, delivered_at))
        c.execute("DELETE FROM showroom WHERE id = ?", (selected[0],))
        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", "Araç başarıyla teslim edildi.")
        window.destroy()

    for i, vehicle in enumerate(vehicles):
        text = f"{vehicle[1]} {vehicle[2]} | {vehicle[3]} | {vehicle[4]} | {vehicle[5]}\u20ba | {vehicle[6]} {vehicle[7]}"
        tk.Button(window, text=text, width=70, anchor="w", command=lambda i=i: submit(i)).pack(pady=3, padx=10, anchor="w")
