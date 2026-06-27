import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import Database
from dialogs import SettingsDialog, TransactionsDialog

class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Parking Management System")
        self.root.geometry("1100x700")
        self.root.configure(bg='#2c3e50')
        self.db = Database()
        self.build_ui()
        self.refresh_grid()
        self.update_clock()
        self.root.after(30000, self.auto_refresh)

    def build_ui(self):
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        for label, cmd in [("Refresh", self.refresh_grid), ("Exit", self.on_exit)]:
            file_menu.add_command(label=label, command=cmd)
        mgmt = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Management", menu=mgmt)
        for label, cmd in [("Settings", self.open_settings), ("All Transactions", self.open_transactions)]:
            mgmt.add_command(label=label, command=cmd)

      
    app = ParkingApp(root)
    root.mainloop()

