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






def initialize_settings(self):
        defaults = {'hourly_rate':'5.0','free_minutes':'15','max_daily_charge':'40.0','currency':'$'}
        for k,v in defaults.items():
            self.cursor.execute('INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)', (k,v))
        self.conn.commit()

    def initialize_spots(self, total=20):
        self.cursor.execute('SELECT COUNT(*) FROM spots')
        if self.cursor.fetchone()[0] == 0:
            for i in range(1, total+1):
                self.cursor.execute('INSERT INTO spots (spot_number, status) VALUES (?,?)', (i,'available'))
            self.conn.commit()

    def get_setting(self, key):
        self.cursor.execute('SELECT value FROM settings WHERE key=?', (key,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def update_setting(self, key, value):
        self.cursor.execute('UPDATE settings SET value=? WHERE key=?', (value,key))
        self.conn.commit()

    def get_all_spots(self):
        self.cursor.execute('SELECT id, spot_number, status FROM spots ORDER BY spot_number')
        return self.cursor.fetchall()

    def occupy_spot(self, spot_id, vehicle_number):
        entry = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        receipt = f'RCP-{random.randint(10000,99999)}-{spot_id}'
        self.cursor.execute('UPDATE spots SET status="occupied" WHERE id=?', (spot_id,))
        self.cursor.execute('''
            INSERT INTO transactions (spot_id, vehicle_number, entry_time, receipt_number)
            VALUES (?,?,?,?)
        ''', (spot_id, vehicle_number, entry, receipt))
        self.conn.commit()
        return receipt

    def free_spot(self, spot_id):
        self.cursor.execute('''
            SELECT id, entry_time, receipt_number, spot_id
            FROM transactions
            WHERE spot_id=? AND exit_time IS NULL
            ORDER BY entry_time DESC LIMIT 1
        ''', (spot_id,))
        trans = self.cursor.fetchone()
        if not trans:
            return None
        tid, entry_str, receipt, _ = trans
        entry = datetime.strptime(entry_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        minutes = (now - entry).total_seconds() / 60

        hourly = float(self.get_setting('hourly_rate'))
        free = float(self.get_setting('free_minutes'))
        maxd = float(self.get_setting('max_daily_charge'))

