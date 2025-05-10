import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from customer_gui import show_customers_via_gui

DB_PATH = "users.db"

# Müşteri Temsilcisi Ekleme Fonksiyonu
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

# Fiyat Teklifi Bekleyen Müşterileri Gösterme
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

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, surname, interested_model 
        FROM customers 
        WHERE offer_requested = 1 AND (proposal_price IS NULL OR proposal_price = '')
    """)
    rows = c.fetchall()

    if not rows:
        tk.Label(scrollable_frame, text="Bekleyen teklif yok.", font=("Arial", 12)).pack(padx=10, pady=10)
        conn.close()
        return

    def submit_offer(customer_id, entry):
        try:
            price = int(entry.get())
            cur = conn.cursor()
            cur.execute("UPDATE customers SET proposal_price = ? WHERE id = ?", (price, customer_id))
            conn.commit()
            messagebox.showinfo("Başarılı", "Teklif kaydedildi.")
            window.destroy()
            show_offer_requests_for_manager(root)
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir sayı girin.")

    for i, row in enumerate(rows, 1):
        cid, name, surname, model = row
        line = tk.Frame(scrollable_frame)
        line.pack(anchor="w", padx=10, pady=5)

        tk.Label(line, text=f"{i}. {name} {surname} | Model: {model}").grid(row=0, column=0, sticky="w")
        entry = tk.Entry(line, width=10)
        entry.grid(row=0, column=1, padx=10)
        tk.Button(line, text="Teklif Gir", command=lambda cid=cid, e=entry: submit_offer(cid, e)).grid(row=0, column=2)

# Test Sürüşü İsteklerini Onaylama
def show_test_drive_requests(root):
    window = tk.Toplevel(root)
    window.title("Test Sürüşü İstekleri")
    window.geometry("600x400")

    tk.Label(window, text="Test Sürüşü Onayı Bekleyen Müşteriler", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, surname, interested_model 
        FROM customers 
        WHERE test_drive_requested = 1 AND (test_drive_approved IS NULL OR test_drive_approved = '')
    """)
    rows = c.fetchall()

    if not rows:
        tk.Label(scrollable_frame, text="Bekleyen test sürüşü isteği yok.", font=("Arial", 12)).pack(padx=10, pady=10)
        conn.close()
        return

    def approve_drive(customer_id):
        cur = conn.cursor()
        cur.execute("UPDATE customers SET test_drive_approved = 1 WHERE id = ?", (customer_id,))
        conn.commit()
        messagebox.showinfo("Onaylandı", "Test sürüşü onaylandı.")
        window.destroy()
        show_test_drive_requests(root)

    for i, row in enumerate(rows, 1):
        cid, name, surname, model = row
        line = tk.Frame(scrollable_frame)
        line.pack(anchor="w", padx=10, pady=5)

        tk.Label(line, text=f"{i}. {name} {surname} | Model: {model}").grid(row=0, column=0, sticky="w")
        tk.Button(line, text="Onayla", command=lambda cid=cid: approve_drive(cid)).grid(row=0, column=1, padx=10)

# Teslim Edilen Araçlar Raporu
def show_delivered_vehicle_report(root):
    window = tk.Toplevel(root)
    window.title("Teslim Edilen Araçlar Raporu")
    window.geometry("700x400")

    tk.Label(window, text="Teslim Edilen Araçlar", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT customer_name, customer_surname, brand, model, year, color, price, delivered_at
        FROM sold_vehicles
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        tk.Label(scrollable_frame, text="Henüz teslim edilmiş araç yok.", font=("Arial", 12)).pack(pady=10)
        return

    for i, row in enumerate(rows, 1):
        name, surname, brand, model, year, color, price, date = row
        info = f"{i}. {name} {surname} | {brand} {model} | {year} | {color} | {price}₺ | Teslimat: {date}"
        tk.Label(scrollable_frame, text=info, anchor="w", justify="left", font=("Arial", 11)).pack(anchor="w", pady=2)

# Yıllık Satış Raporu
def show_sales_report(root):
    window = tk.Toplevel(root)
    window.title("Yıllık Satış Raporu")
    window.geometry("700x400")

    tk.Label(window, text="Yıllık Satış Raporu", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(""" 
        SELECT 
            s.brand, 
            s.model, 
            sv.year AS model_year, 
            strftime('%Y', sv.delivered_at) AS sale_year, 
            COUNT(*) AS total_sales
        FROM 
            sold_vehicles sv
        JOIN 
            showroom s 
        ON 
            sv.brand = s.brand AND sv.model = s.model
        GROUP BY 
            s.brand, s.model, sv.year, strftime('%Y', sv.delivered_at)
        ORDER BY 
            sale_year
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        tk.Label(scrollable_frame, text="Rapor verisi bulunamadı.", font=("Arial", 12)).pack(padx=10, pady=10)
        return

    for i, row in enumerate(rows, 1):
        brand, model, model_year, sale_year, total_sales = row
        info = f"{i}. {brand} {model} {model_year} | Satış Yılı: {sale_year} | Toplam Satış: {total_sales}"
        tk.Label(scrollable_frame, text=info, anchor="w", justify="left", font=("Arial", 11)).pack(anchor="w", pady=2)

def open_manager_panel(user_id):
    window = tk.Tk()
    window.title("Müdür Paneli")
    window.geometry("420x600")

    tk.Label(window, text=f"Giriş Yapan: {user_id} (Müdür)", font=("Arial", 12, "bold")).pack(pady=15)

    tk.Button(window, text="Raporları Gör (Kayıtlı Müşteriler)", width=35, command=lambda: show_customers_via_gui(window)).pack(pady=10)
    tk.Button(window, text="Müşteri Tekliflerini Gör / Teklif Ver", width=35, command=lambda: show_offer_requests_for_manager(window)).pack(pady=10)
    tk.Button(window, text="Test Sürüşü İsteklerini Onayla", width=35, command=lambda: show_test_drive_requests(window)).pack(pady=10)
    tk.Button(window, text="Teslim Edilen Araç Raporu", width=35, command=lambda: show_delivered_vehicle_report(window)).pack(pady=10)
    tk.Button(window, text="Yıllık Satış Raporu", width=35, command=lambda: show_sales_report(window)).pack(pady=10)
    tk.Button(window, text="Müşteri Temsilcisi Ekle", width=35, command=add_agent).pack(pady=10)
    tk.Button(window, text="Çıkış", width=35, command=window.destroy).pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    open_manager_panel("1")
