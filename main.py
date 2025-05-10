import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import subprocess
import sys

DB_PATH = "users.db"

def login(role):
    user_id = simpledialog.askstring("Giriş", "Kullanıcı ID:")
    password = simpledialog.askstring("Giriş", "Şifre:", show="*")
    if not user_id or not password:
        messagebox.showerror("Hata", "ID ve şifre boş olamaz.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=? AND password=? AND role=?", (user_id, password, role))
    if c.fetchone():
        root.withdraw()  # root.destroy() yerine pencereyi gizle
        subprocess.Popen([sys.executable, "main_gui.py", user_id, role])
    else:
        messagebox.showerror("Giriş Hatalı", "ID, şifre veya rol hatalı.")
    conn.close()

root = tk.Tk()
root.title("Araç Satış Sistemi Giriş")
root.geometry("350x200")

tk.Label(root, text="Giriş Türünü Seçin", font=("Arial", 12, "bold")).pack(pady=10)

tk.Button(root, text="Müşteri Temsilcisi Girişi", width=35,
          command=lambda: login("agent")).pack(pady=10)

tk.Button(root, text="Müdür Girişi", width=35,
          command=lambda: login("manager")).pack(pady=10)

root.mainloop()