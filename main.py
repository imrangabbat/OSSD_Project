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

        # Right – grid with scroll
        right = tk.Frame(main, bg='#2c3e50')
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(right, bg='#2c3e50', highlightthickness=0)
        scroll = ttk.Scrollbar(right, orient=tk.VERTICAL, command=canvas.yview)
        self.grid_frame = tk.Frame(canvas, bg='#2c3e50')
        self.grid_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status = tk.Frame(self.root, bg='#34495e', height=25)
        status.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(status, textvariable=self.status_var, bg='#34495e', fg='white').pack(side=tk.LEFT, padx=10)
        self.time_var = tk.StringVar()
        tk.Label(status, textvariable=self.time_var, bg='#34495e', fg='white').pack(side=tk.RIGHT, padx=10)

    def refresh_grid(self):
        for w in self.grid_frame.winfo_children(): w.destroy()
        spots = self.db.get_all_spots()
        cols = 5
        for i, (sid, num, status) in enumerate(spots):
            btn = tk.Button(self.grid_frame, text=f"Spot {num}\n{status.upper()}", width=12, height=4,
                            bg='#2ecc71' if status=='available' else '#e74c3c', fg='white',
                            font=('Arial',10,'bold'), relief=tk.RAISED,
                            command=lambda s=sid, st=status: self.spot_click(s, st))
            btn.grid(row=i//cols, column=i%cols, padx=5, pady=5, sticky='nsew')
        self.update_stats()
        self.status_var.set(f"Updated: {datetime.now().strftime('%H:%M:%S')}")

    def update_stats(self):
        for w in self.stats_frame.winfo_children(): w.destroy()
        total = self.db.cursor.execute('SELECT COUNT(*) FROM spots').fetchone()[0]
        occ = self.db.cursor.execute('SELECT COUNT(*) FROM spots WHERE status="occupied"').fetchone()[0]
        rev = self.db.get_daily_revenue(datetime.now().strftime('%Y-%m-%d'))
        for label, val in [("Total Spots", total), ("Occupied", occ), ("Available", total-occ), ("Today's Revenue", f"${rev:.2f}")]:
            f = tk.Frame(self.stats_frame, bg='#34495e')
            f.pack(fill=tk.X, pady=2)
            tk.Label(f, text=label, bg='#34495e', fg='#bdc3c7', font=('Arial',10)).pack(side=tk.LEFT)
            tk.Label(f, text=str(val), bg='#34495e', fg='white', font=('Arial',12,'bold')).pack(side=tk.RIGHT)

    def spot_click(self, spot_id, status):
        if status == 'available':
            self.enter_vehicle(spot_id)
        else:
            self.exit_vehicle(spot_id)

    def enter_vehicle(self, spot_id):
        d = tk.Toplevel(self.root)
        d.title("Vehicle Entry")
        d.geometry("400x200")
        d.transient(self.root); d.grab_set()
        tk.Label(d, text="Enter Vehicle Number", font=('Arial',14)).pack(pady=10)
        v = tk.StringVar()
        tk.Entry(d, textvariable=v, font=('Arial',14), width=20).pack(pady=5)
        def confirm():
            vnum = v.get().strip()
            if not vnum:
                messagebox.showerror("Error", "Vehicle number required")
                return
            self.db.cursor.execute('SELECT id FROM transactions WHERE vehicle_number=? AND exit_time IS NULL', (vnum,))
            if self.db.cursor.fetchone():
                messagebox.showerror("Error", f"Vehicle {vnum} already parked")
                return
            rec = self.db.occupy_spot(spot_id, vnum)
            messagebox.showinfo("Success", f"Parked {vnum}\nReceipt: {rec}")
            d.destroy()
            self.refresh_grid()
        tk.Button(d, text="Park", command=confirm, bg='#2ecc71', fg='white', font=('Arial',12)).pack(pady=15)
        tk.Button(d, text="Cancel", command=d.destroy, bg='#e74c3c', fg='white', font=('Arial',12)).pack()

    def exit_vehicle(self, spot_id):
        self.db.cursor.execute('''
            SELECT id, vehicle_number, entry_time FROM transactions
            WHERE spot_id=? AND exit_time IS NULL ORDER BY entry_time DESC LIMIT 1
        ''', (spot_id,))
        trans = self.db.cursor.fetchone()
        if not trans:
            messagebox.showerror("Error", "No active transaction")
            return
        tid, vnum, entry = trans
        d = tk.Toplevel(self.root)
        d.title("Vehicle Exit")
        d.geometry("500x350")
        d.transient(self.root); d.grab_set()
        tk.Label(d, text=f"Vehicle: {vnum}", font=('Arial',14,'bold')).pack(pady=5)
        tk.Label(d, text=f"Entry: {entry}", font=('Arial',12)).pack()
        now = datetime.now()
        tk.Label(d, text=f"Current: {now.strftime('%Y-%m-%d %H:%M:%S')}", font=('Arial',12)).pack()
        mins = (now - datetime.strptime(entry, '%Y-%m-%d %H:%M:%S')).total_seconds()/60
        tk.Label(d, text=f"Duration: {mins:.1f} min", font=('Arial',12)).pack()
        def confirm():
            res = self.db.free_spot(spot_id)
            if res:
                msg = (f"Exit confirmed\n\nReceipt: {res['receipt']}\nVehicle: {res['vehicle']}\n"
                       f"Spot: {res['spot_number']}\nDuration: {res['duration_minutes']} min\nFee: ${res['fee']:.2f}")
                messagebox.showinfo("Exit Summary", msg)
                d.destroy()
                self.refresh_grid()
            else:
                messagebox.showerror("Error", "Could not process exit")
        tk.Label(d, text="Proceed with exit?", font=('Arial',12)).pack(pady=10)
        tk.Button(d, text="Confirm Exit", command=confirm, bg='#f1c40f', fg='black', font=('Arial',12)).pack(pady=5)
        tk.Button(d, text="Cancel", command=d.destroy, bg='#e74c3c', fg='white', font=('Arial',12)).pack(pady=5)

    def update_clock(self):
        self.time_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def auto_refresh(self):
        self.refresh_grid()
        self.root.after(30000, self.auto_refresh)

    def open_settings(self):
        SettingsDialog(self.root, self.db, self.refresh_grid)

    def open_transactions(self):
        TransactionsDialog(self.root, self.db)

    def on_exit(self):
        if messagebox.askyesno("Exit", "Are you sure?"):
            self.db.close()
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()

