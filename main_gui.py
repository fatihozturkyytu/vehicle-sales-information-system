import tkinter as tk
import sys
import sqlite3
from tkinter import simpledialog, messagebox
import subprocess
from showroom_gui import open_showroom_gui
from customer_gui import (
    add_customer_via_form,
    show_customers_via_gui,
    show_offer_requests_for_manager,
    show_proposed_customers_for_agent,
    show_test_drive_statuses
)
from manager_gui import open_manager_panel
from delivery_gui import deliver_sold_vehicle
from tkinter import Label
from PIL import Image, ImageTk
import os

# Komut satırı parametresi kontrolü
if len(sys.argv) >= 3:
    user_id = sys.argv[1]
    role = sys.argv[2]
else:
    user_id = "demo_kullanici"
    role = "agent"  # test amaçlı

DB_PATH = "users.db"

# Veritabanı tablo kontrolleri
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    interested_model TEXT NOT NULL,
    offer_requested INTEGER NOT NULL CHECK(offer_requested IN (0,1)),
    proposal_price INTEGER,
    test_drive_requested INTEGER DEFAULT 0,
    test_drive_approved INTEGER
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('agent', 'manager'))
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS sold_vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    year TEXT NOT NULL,
    color TEXT NOT NULL,
    price TEXT NOT NULL,
    customer_name TEXT,
    customer_surname TEXT,
    sold_at TEXT NOT NULL
)
""")
conn.commit()
conn.close()

# Temsilci ekleme (müdür yetkisiyle)
def add_agent():
    new_id = simpledialog.askstring("Yeni Temsilci", "Temsilci ID:")
    new_pw = simpledialog.askstring("Yeni Temsilci", "Şifre:")
    if not new_id or not new_pw:
        messagebox.showerror("Hata", "Boş alan bırakmayın.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (id, password, role) VALUES (?, ?, ?)", (new_id, new_pw, 'agent'))
        conn.commit()
        messagebox.showinfo("Başarılı", "Müşteri Temsilcisi başarıyla eklendi.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Hata", "Bu ID zaten mevcut.")
    conn.close()

# Araç & stok arayüzü
def open_vehicle_gui():
    subprocess.Popen([sys.executable, "vehicle_and_stock.py"])

# === Girişe göre GUI ===
if role == "manager":
    open_manager_panel(user_id)
else:
    root = tk.Tk()
    root.title("Borusan Oto BMW")
    # Load BMW logo image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "bmw.svg.png")
    original_logo = Image.open(image_path).resize((120, 120))  # Adjust size as needed
    logo_img = ImageTk.PhotoImage(original_logo)

    # Left logo
    logo_label_left = Label(root, image=logo_img)
    logo_label_left.image = logo_img  # Keep a reference!
    logo_label_left.pack(side="left", padx=20, pady=20)

    # Right logo
    logo_label_right = Label(root, image=logo_img)
    logo_label_right.image = logo_img
    logo_label_right.pack(side="right", padx=20, pady=20)

    tk.Label(root, text=f"Giriş Yapan: {user_id} (Müşteri Temsilcisi)", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(root, text="Müşteri Ekle", width=30, command=lambda: add_customer_via_form(root)).pack(pady=10)
    tk.Button(root, text="Kayıtlı Müşterileri Göster", width=30, command=lambda: show_customers_via_gui(root)).pack(pady=5)
    tk.Button(root, text="Fiyat Teklifi Verilenler", width=30, command=lambda: show_proposed_customers_for_agent(root)).pack(pady=5)
    tk.Button(root, text="Test Sürüşü İstek Durumları", width=30, command=lambda: show_test_drive_statuses(root)).pack(pady=5)
    tk.Button(root, text="Araç ve Stok Yönetimi", width=30, command=open_vehicle_gui).pack(pady=10)
    tk.Button(root, text="Showroom'daki Araçları Gör", width=30, command=open_showroom_gui).pack(pady=5)
    tk.Button(root, text="Showroom'daki Aracı Teslim Et", width=30, command=lambda: deliver_sold_vehicle(root)).pack(pady=5)

    tk.Button(root, text="Çıkış", width=15, command=root.destroy).pack(pady=20)
    root.mainloop()
