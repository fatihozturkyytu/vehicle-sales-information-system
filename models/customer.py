import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_PATH = "users.db"

# === GUI Fonksiyonu: Müşteri Ekle ===
def add_customer_via_form(root):
    def submit():
        name = entry_name.get()
        surname = entry_surname.get()
        model = entry_model.get()
        offer = var_offer.get()

        if not name or not surname or not model:
            messagebox.showerror("Hata", "Tüm alanları doldurun.")
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT INTO customers 
                     (name, surname, interested_model, offer_requested) 
                     VALUES (?, ?, ?, ?)""",
                  (name, surname, model, offer))
        conn.commit()
        conn.close()
        messagebox.showinfo("Başarılı", "Müşteri başarıyla eklendi.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Müşteri Ekle")

    tk.Label(window, text="Ad:").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(window)
    entry_name.grid(row=0, column=1)

    tk.Label(window, text="Soyad:").grid(row=1, column=0, padx=10, pady=5)
    entry_surname = tk.Entry(window)
    entry_surname.grid(row=1, column=1)

    tk.Label(window, text="İlgilendiği Model:").grid(row=2, column=0, padx=10, pady=5)
    entry_model = tk.Entry(window)
    entry_model.grid(row=2, column=1)

    var_offer = tk.IntVar()
    tk.Checkbutton(window, text="Fiyat Teklifi İsteniyor", variable=var_offer).grid(row=3, columnspan=2, pady=5)

    tk.Button(window, text="Kaydet", command=submit).grid(row=4, columnspan=2, pady=10)


# === GUI Fonksiyonu: Müşterileri Listele ===
def show_customers_via_gui(root):
    window = tk.Toplevel(root)
    window.title("Kayıtlı Müşteriler")
    window.geometry("500x400")

    tk.Label(window, text="Kayıtlı Müşteriler", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, surname, interested_model, offer_requested FROM customers")
    rows = c.fetchall()
    conn.close()

    if not rows:
        tk.Label(scrollable_frame, text="Kayıtlı müşteri yok.", font=("Arial", 12)).pack(pady=10)
        return

    for i, row in enumerate(rows, 1):
        name, surname, model, offer = row
        offer_text = "Evet" if offer else "Hayır"
        info = f"{i}. {name} {surname} | Model: {model} | Teklif: {offer_text}"
        tk.Label(scrollable_frame, text=info, anchor="w", justify="left", font=("Arial", 11)).pack(anchor="w", pady=2)


# === GUI Fonksiyonu: Teklif Girildikten Sonra Pencereyi Yenileme ===
def refresh_offer_window(root):
    window = tk.Toplevel(root)
    window.title("Fiyat Teklifi Güncelle")
    tk.Label(window, text="Teklif güncellendi.", font=("Arial", 12)).pack(pady=20)
    tk.Button(window, text="Kapat", command=window.destroy).pack(pady=10)


# === Yardımcı Fonksiyon: Temiz Sayı Girişi Doğrulama ===
def is_valid_price(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
