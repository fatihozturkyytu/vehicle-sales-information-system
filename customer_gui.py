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
        test_drive = var_test_drive.get()

        if not name or not surname or not model:
            messagebox.showerror("Hata", "Tüm alanları doldurun.")
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT INTO customers 
                     (name, surname, interested_model, offer_requested, test_drive_requested) 
                     VALUES (?, ?, ?, ?, ?)""",
                  (name, surname, model, offer, test_drive))
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

    var_test_drive = tk.IntVar()
    tk.Checkbutton(window, text="Test Sürüşü İsteniyor", variable=var_test_drive).grid(row=4, columnspan=2, pady=5)

    tk.Button(window, text="Kaydet", command=submit).grid(row=5, columnspan=2, pady=10)

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


# === Müdür: Teklif Bekleyen Müşterileri Göster ===
def show_offer_requests_for_manager(root):
    window = tk.Toplevel(root)
    window.title("Fiyat Teklifi Bekleyen Müşteriler")
    window.geometry("600x400")

    tk.Label(window, text="Fiyat Teklifi Bekleyen Müşteriler", font=("Arial", 14, "bold")).pack(pady=10)

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
    refresh_offer_requests_ui(scrollable_frame, conn)


def refresh_offer_requests_ui(frame, conn):
    for widget in frame.winfo_children():
        widget.destroy()

    c = conn.cursor()
    c.execute("""
        SELECT id, name, surname, interested_model 
        FROM customers 
        WHERE offer_requested = 1 AND (proposal_price IS NULL OR proposal_price = '')
    """)
    rows = c.fetchall()

    if not rows:
        tk.Label(frame, text="Bekleyen teklif yok.", font=("Arial", 12)).pack(padx=10, pady=10)
        return

    for i, row in enumerate(rows, 1):
        cid, name, surname, model = row
        line = tk.Frame(frame)
        line.pack(anchor="w", padx=10, pady=5)

        tk.Label(line, text=f"{i}. {name} {surname} | Model: {model}").grid(row=0, column=0, sticky="w")
        entry = tk.Entry(line, width=10)
        entry.grid(row=0, column=1, padx=10)
        tk.Button(line, text="Teklif Gir", command=lambda cid=cid, e=entry: submit_offer(cid, e, conn, frame)).grid(row=0, column=2)


def submit_offer(customer_id, entry, conn, frame):
    try:
        price = int(entry.get())
        cur = conn.cursor()
        cur.execute("UPDATE customers SET proposal_price = ? WHERE id = ?", (price, customer_id))
        conn.commit()
        messagebox.showinfo("Başarılı", "Teklif kaydedildi.")
        refresh_offer_requests_ui(frame, conn)
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")


# === GUI Fonksiyonu: Temsilci için Fiyat Verilmişleri Göster ===
def show_proposed_customers_for_agent(root):
    window = tk.Toplevel(root)
    window.title("Fiyat Teklifi Verilmiş Müşteriler")
    window.geometry("500x400")

    tk.Label(window, text="Fiyat Teklifi Verilmiş Müşteriler", font=("Arial", 14, "bold")).pack(pady=10)

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

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT name, surname, interested_model, proposal_price 
            FROM customers 
            WHERE proposal_price IS NOT NULL AND proposal_price != ''
        """)
        rows = c.fetchall()
        conn.close()
    except Exception as e:
        messagebox.showerror("Hata", f"Veritabanı hatası:\n{e}")
        return

    if not rows:
        tk.Label(scrollable_frame, text="Fiyat teklifi yapılmış müşteri yok.", font=("Arial", 12)).pack(pady=10)
        return

    for i, row in enumerate(rows, 1):
        name, surname, model, price = row
        info = f"{i}. {name} {surname} | Model: {model} | Teklif: {price}₺"
        tk.Label(scrollable_frame, text=info, anchor="w", justify="left", font=("Arial", 11)).pack(anchor="w", pady=2)

def show_test_drive_statuses(root):
    window = tk.Toplevel(root)
    window.title("Test Sürüşü İstek Durumları")
    window.geometry("500x400")

    tk.Label(window, text="Test Sürüşü Durumları", font=("Arial", 14, "bold")).pack(pady=10)

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
    c.execute("""
        SELECT name, surname, interested_model, test_drive_requested, test_drive_approved
        FROM customers
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        tk.Label(scrollable_frame, text="Kayıt bulunamadı.", font=("Arial", 12)).pack(pady=10)
        return

    for i, row in enumerate(rows, 1):
        name, surname, model, requested, approved = row

        if not requested:
            status = "İstenmedi"
        elif approved:
            status = "Onaylandı"
        else:
            status = "Bekliyor"

        info = f"{i}. {name} {surname} | Model: {model} | Test Sürüşü: {status}"
        tk.Label(scrollable_frame, text=info, anchor="w", justify="left", font=("Arial", 11)).pack(anchor="w", pady=2)
