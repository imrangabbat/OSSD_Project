import sqlite3
from datetime import datetime
import random

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('parking_system.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.initialize_settings()
        self.initialize_spots()

    def create_tables(self):
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS spots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spot_number INTEGER UNIQUE NOT NULL,
                status TEXT DEFAULT 'available'
            );
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spot_id INTEGER,
                vehicle_number TEXT NOT NULL,
                entry_time TIMESTAMP,
                exit_time TIMESTAMP,
                fee REAL DEFAULT 0,
                receipt_number TEXT UNIQUE,
                FOREIGN KEY (spot_id) REFERENCES spots (id)
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        ''')
        self.conn.commit()

   
    def close(self):
        self.conn.close()
