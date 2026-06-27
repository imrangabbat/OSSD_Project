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

    
