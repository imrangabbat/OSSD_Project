import tkinter as tk
from tkinter import ttk, messagebox

class SettingsDialog:
    def __init__(self, parent, db, refresh_callback):
        self.db = db
        self.refresh = refresh_callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

    



tk.Label(self.dialog, text="Parking Settings", font=('Arial',16,'bold')).pack(pady=10)

        frames = []
        labels = ["Hourly Rate ($):", "Free Minutes:", "Max Daily Charge ($):"]
        keys = ['hourly_rate', 'free_minutes', 'max_daily_charge']
        self.vars = {}

        for lbl, key in zip(labels, keys):
            f = tk.Frame(self.dialog)
            f.pack(fill=tk.X, padx=20, pady=5)
            tk.Label(f, text=lbl, width=20, anchor='w').pack(side=tk.LEFT)
            self.vars[key] = tk.StringVar(value=db.get_setting(key))
            tk.Entry(f, textvariable=self.vars[key], width=10).pack(side=tk.LEFT)

        def save():
            try:
                for key in keys:
                    val = float(self.vars[key].get())
                    if val < 0: raise ValueError
                    self.db.update_setting(key, str(val))
                messagebox.showinfo("Success", "Settings updated")
                self.refresh()
                self.dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid positive numbers")

        tk.Button(self.dialog, text="Save Settings", command=save,
                  bg='#2ecc71', fg='white', font=('Arial',12)).pack(pady=20)
        tk.Button(self.dialog, text="Cancel", command=self.dialog.destroy,
                  bg='#e74c3c', fg='white', font=('Arial',12)).pack()


class TransactionsDialog:
    def _init_(self, parent, db):
        self.db = db
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("All Transactions")
        self.dialog.geometry("900x500")
        self.dialog.transient(parent)

        # Filter
        filter_frame = tk.Frame(self.dialog)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(filter_frame, text="Filter by Date (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.date_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=self.date_var, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Apply", command=self.load_transactions).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Show All", command=lambda: (self.date_var.set(''), self.load_transactions())).pack(side=tk.LEFT)

        # Treeview
        cols = ('ID','Spot','Vehicle','Entry','Exit','Fee','Receipt')
        self.tree = ttk.Treeview(self.dialog, columns=cols, show='headings', height=20)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        scroll = ttk.Scrollbar(self.dialog, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_transactions()

   
