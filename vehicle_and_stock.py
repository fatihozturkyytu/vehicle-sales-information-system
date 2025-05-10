import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from models.vehicle import Vehicle
from models.stock import Stock
from models.showroom import Showroom

selected_vehicle = None
selected_stock = None
visible_model_list = []

Vehicle.init_db()
Stock.init_db()
Showroom.init_db()

def gui_add_vehicle():
    vehicle, error = Vehicle.add(entry_brand.get(), entry_model.get())
    if error:
        messagebox.showerror("Hata", error)
    else:
        refresh_model_list(Vehicle.get_all())
        entry_brand.delete(0, tk.END)
        entry_model.delete(0, tk.END)

def gui_confirm_selected_model():
    global selected_vehicle
    selection = model_listbox.curselection()
    if not selection:
        messagebox.showerror("Hata", "Lütfen listeden bir model seçin.")
        return
    selected_vehicle = visible_model_list[selection[0]]
    label_selected_model.config(text=f"Seçilen Model: {selected_vehicle}")
    update_stock_list_for_selected_vehicle()

def gui_add_stock():
    if not selected_vehicle:
        messagebox.showerror("Hata", "Önce bir model seçin ve 'Modeli Seç' butonuna basın.")
        return

    stock, error = Stock.add_or_prompt_update(
        selected_vehicle,
        entry_year.get(),
        entry_color.get(),
        entry_price.get(),
        entry_quantity.get()
    )

    if error:
        messagebox.showerror("Hata", error)

    update_stock_list_for_selected_vehicle()
    entry_year.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)

def refresh_model_list(vehicles):
    global visible_model_list
    visible_model_list = vehicles
    model_listbox.delete(0, tk.END)
    for v in vehicles:
        model_listbox.insert(tk.END, str(v))

def update_stock_list_for_selected_vehicle():
    global selected_stock
    selected_stock = None
    stock_listbox.delete(0, tk.END)
    if not selected_vehicle:
        return

    filtered = [s for s in Stock.filter_by_vehicle(selected_vehicle) if s.quantity > 0]
    for stock in filtered:
        stock_listbox.insert(tk.END, str(stock))

def gui_select_stock(event=None):
    global selected_stock
    selection = stock_listbox.curselection()
    if not selection or not selected_vehicle:
        selected_stock = None
        return
    filtered = [s for s in Stock.filter_by_vehicle(selected_vehicle) if s.quantity > 0]
    selected_stock = filtered[selection[0]]

from tkinter import simpledialog, messagebox
from datetime import datetime
import sqlite3
from showroom_gui import Showroom
from models.stock import Stock

def gui_send_to_dealer_purpose(purpose):
    selection = stock_listbox.curselection()
    if not selection:
        messagebox.showerror("Hata", "Lütfen önce stoktan bir araç seçin.")
        return

    filtered = [s for s in Stock.filter_by_vehicle(selected_vehicle) if s.quantity > 0]
    selected_stock_local = filtered[selection[0]]

    if selected_stock_local.quantity <= 0:
        messagebox.showerror("Uyarı", "Bu stokta ürün kalmamış.")
        return

    if purpose == "Sipariş Üzerine":
        # Sipariş üzerine çekildiğinde tarih istemeyeceğiz
        name = simpledialog.askstring("Müşteri Adı", "Müşteri adı:")
        surname = simpledialog.askstring("Müşteri Soyadı", "Müşteri soyadı:")
        price = simpledialog.askfloat("Satış Fiyatı", "Araç satış fiyatı (₺):")

        if not name or not surname or price is None:
            messagebox.showerror("Hata", "Tüm müşteri bilgileri girilmeli.")
            return

        # Stok adedini düş
        selected_stock_local.quantity -= 1
        Stock._update_db_quantity(selected_stock_local)

        # Showroom'a ekle
        Showroom.add_sales_vehicle(selected_stock_local, name, surname, price, None)  # Tarih alınmayacak
        update_stock_list_for_selected_vehicle()
        messagebox.showinfo("Başarılı", "Araç bayiye sipariş üzerine çekildi.")
        open_showroom_window("Satış Amaçlı Araçlar")

    elif purpose == "Gösterim Amaçlı":
        selected_stock_local.quantity -= 1
        Stock._update_db_quantity(selected_stock_local)
        Showroom.add_display_vehicle(selected_stock_local)
        update_stock_list_for_selected_vehicle()
        messagebox.showinfo("Başarılı", "Araç bayiye gösterim amaçlı çekildi.")
        open_showroom_window("Sergilenen Araçlar")

def gui_search_model():
    query = entry_search.get().strip().lower()
    if not query:
        refresh_model_list(Vehicle.get_all())
    else:
        filtered = [v for v in Vehicle.get_all() if query in v.brand.lower() or query in v.model.lower()]
        refresh_model_list(filtered)

def open_showroom_window(purpose):
    win = tk.Toplevel()
    win.title("Showroom - " + purpose)

    if purpose == "Sergilenen Araçlar":
        items = Showroom.get_display_vehicles()
    else:
        items = Showroom.get_sales_vehicles()

    for item in items:
        tk.Label(win, text=item.to_showroom_string()).pack(anchor="w", padx=10)

    tk.Button(win, text="Geri Dön", command=win.destroy).pack(pady=10)

# === GUI ===
root = tk.Tk()
root.title("Araç ve Stok Yönetimi")

frame_model = tk.LabelFrame(root, text="Model Ekle")
frame_model.pack(padx=10, pady=5, fill="x")

entry_brand = tk.Entry(frame_model)
tk.Label(frame_model, text="Marka:").grid(row=0, column=0)
entry_brand.grid(row=0, column=1)

entry_model = tk.Entry(frame_model)
tk.Label(frame_model, text="Model:").grid(row=1, column=0)
entry_model.grid(row=1, column=1)

tk.Button(frame_model, text="Model Ekle", command=gui_add_vehicle).grid(row=2, columnspan=2)

model_listbox = tk.Listbox(frame_model)
model_listbox.grid(row=3, columnspan=2, pady=5)

label_selected_model = tk.Label(frame_model, text="Seçilen Model: -")
label_selected_model.grid(row=4, columnspan=2)

tk.Button(frame_model, text="Modeli Seç", command=gui_confirm_selected_model).grid(row=5, columnspan=2)

tk.Label(frame_model, text="Model Ara:").grid(row=6, column=0)
entry_search = tk.Entry(frame_model)
entry_search.grid(row=6, column=1)
tk.Button(frame_model, text="Ara", command=gui_search_model).grid(row=7, columnspan=2, pady=3)

frame_stock = tk.LabelFrame(root, text="Stok Ekle")
frame_stock.pack(padx=10, pady=5, fill="x")

entry_year = tk.Entry(frame_stock)
tk.Label(frame_stock, text="Yıl:").grid(row=0, column=0)
entry_year.grid(row=0, column=1)

entry_color = tk.Entry(frame_stock)
tk.Label(frame_stock, text="Renk:").grid(row=1, column=0)
entry_color.grid(row=1, column=1)

entry_price = tk.Entry(frame_stock)
tk.Label(frame_stock, text="Fiyat:").grid(row=2, column=0)
entry_price.grid(row=2, column=1)

entry_quantity = tk.Entry(frame_stock)
tk.Label(frame_stock, text="Adet:").grid(row=3, column=0)
entry_quantity.grid(row=3, column=1)

tk.Button(frame_stock, text="Stok Ekle", command=gui_add_stock).grid(row=4, columnspan=2)

stock_listbox = tk.Listbox(frame_stock, width=80)
stock_listbox.grid(row=5, columnspan=2, pady=5)
stock_listbox.bind("<<ListboxSelect>>", gui_select_stock)

tk.Button(frame_stock, text="Bayiye Sipariş Üzerine Çek", command=lambda: gui_send_to_dealer_purpose("Sipariş Üzerine")).grid(row=6, columnspan=2)
tk.Button(frame_stock, text="Bayiye Gösterim Amaçlı Çek", command=lambda: gui_send_to_dealer_purpose("Gösterim Amaçlı")).grid(row=7, columnspan=2)

refresh_model_list(Vehicle.get_all())
root.mainloop()
