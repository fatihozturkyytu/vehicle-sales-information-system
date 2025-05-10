import tkinter as tk
from models.showroom import Showroom

def open_showroom_gui():
    win = tk.Tk()
    win.title("Showroom'daki Araçlar")

    # Başlık
    tk.Label(win, text="Showroom'daki Araçlar", font=("Arial", 14, "bold")).pack(pady=10)

    # Sergilenen Araçlar
    frame_display = tk.LabelFrame(win, text="Sergilenen Araçlar")
    frame_display.pack(padx=10, pady=5, fill="both", expand=True)

    display_vehicles = Showroom.get_display_vehicles()
    if not display_vehicles:
        tk.Label(frame_display, text="Sergilenen araç yok.").pack()
    else:
        for vehicle in display_vehicles:
            tk.Label(frame_display, text=vehicle.to_showroom_string()).pack(anchor="w", padx=10)

    # Satış Amaçlı Araçlar
    frame_sales = tk.LabelFrame(win, text="Satış Amaçlı Araçlar")
    frame_sales.pack(padx=10, pady=5, fill="both", expand=True)

    sales_vehicles = Showroom.get_sales_vehicles()
    if not sales_vehicles:
        tk.Label(frame_sales, text="Satış amaçlı araç yok.").pack()
    else:
        for vehicle in sales_vehicles:
            tk.Label(frame_sales, text=vehicle.to_showroom_string()).pack(anchor="w", padx=10)

    # Geri Dön
    tk.Button(win, text="Geri Dön", command=win.destroy).pack(pady=10)

    win.mainloop()
