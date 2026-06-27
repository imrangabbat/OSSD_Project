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

        if minutes <= free:
            fee = 0.0
        else:
            fee = (minutes - free) / 60 * hourly
            if fee > maxd:
                fee = maxd
            fee = round(fee, 2)

        exit_str = now.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('UPDATE transactions SET exit_time=?, fee=? WHERE id=?', (exit_str,fee,tid))
        self.cursor.execute('UPDATE spots SET status="available" WHERE id=?', (spot_id,))
        self.conn.commit()

        return {
            'receipt': receipt,
            'vehicle': self.cursor.execute('SELECT vehicle_number FROM transactions WHERE id=?',(tid,)).fetchone()[0],
            'entry_time': entry_str,
            'exit_time': exit_str,
            'duration_minutes': round(minutes,1),
            'fee': fee,
            'spot_number': self.cursor.execute('SELECT spot_number FROM spots WHERE id=?',(spot_id,)).fetchone()[0]
        }

    def get_transactions(self, limit=100, date_filter=None):
        query = '''
            SELECT t.id, t.vehicle_number, t.entry_time, t.exit_time, t.fee,
                   t.receipt_number, s.spot_number
            FROM transactions t
            JOIN spots s ON t.spot_id = s.id
            WHERE t.exit_time IS NOT NULL
        '''
        params = []
        if date_filter:
            query += ' AND DATE(t.entry_time) = ?'
            params.append(date_filter)
        query += ' ORDER BY t.entry_time DESC LIMIT ?'
        params.append(limit)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_daily_revenue(self, date_str):
        self.cursor.execute('SELECT COALESCE(SUM(fee),0) FROM transactions WHERE DATE(entry_time)=? AND exit_time IS NOT NULL', (date_str,))
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()
