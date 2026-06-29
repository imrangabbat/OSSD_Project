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





# Main layout
        main = tk.Frame(self.root, bg='#2c3e50')
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel
        left = tk.Frame(main, bg='#34495e', width=300)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        left.pack_propagate(False)
        tk.Label(left, text="Parking Info", font=('Arial',16,'bold'), bg='#34495e', fg='white').pack(pady=10)
        self.stats_frame = tk.Frame(left, bg='#34495e')
        self.stats_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(left, text="Quick Actions", font=('Arial',14,'bold'), bg='#34495e', fg='white').pack(pady=(20,5))
        btn_frame = tk.Frame(left, bg='#34495e')
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        for txt, cmd, col in [("🔄 Refresh", self.refresh_grid, '#1abc9c'),
                              ("📋 All Transactions", self.open_transactions, '#3498db'),
                              ("⚙️ Settings", self.open_settings, '#e67e22')]:
            tk.Button(btn_frame, text=txt, command=cmd, bg=col, fg='white', font=('Arial',12)).pack(fill=tk.X, pady=2)

        # Legend
        leg = tk.Frame(left, bg='#34495e')
        leg.pack(pady=20, fill=tk.X, padx=10)
        tk.Label(leg, text="Legend", font=('Arial',14,'bold'), bg='#34495e', fg='white').pack(anchor='w')
        for color, label in [('#2ecc71','Available'), ('#e74c3c','Occupied')]:
            f = tk.Frame(leg, bg='#34495e')
            f.pack(anchor='w', pady=2)
            tk.Label(f, bg=color, width=4, height=1, relief=tk.RAISED).pack(side=tk.LEFT)
            tk.Label(f, text=label, bg='#34495e', fg='white', font=('Arial',10)).pack(side=tk.LEFT, padx=5)

      

if _name_ == "_main_":
    root = tk.Tk()
