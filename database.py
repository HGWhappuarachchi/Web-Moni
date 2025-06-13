# database.py
import sqlite3
import os
import sys

def get_base_path():
    """ Get the base path, for use with PyInstaller bundles """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(get_base_path(), 'monitor_app.db')

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Creates or updates the database tables with all necessary columns."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- THIS IS THE CORRECTED SCHEMA WITH NO PLACEHOLDERS ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL UNIQUE,
        description TEXT,
        widget_pos_x INTEGER DEFAULT 100,
        widget_pos_y INTEGER DEFAULT 100,
        widget_size TEXT DEFAULT 'Medium',
        widget_ontop INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS email_settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        sender_email TEXT DEFAULT '',
        sender_password TEXT DEFAULT ''
    )
    ''')
    
    cursor.execute('INSERT OR IGNORE INTO email_settings (id) VALUES (1)')
    
    # Safely add new columns to the ips table if they don't already exist
    table_info = cursor.execute("PRAGMA table_info(ips)").fetchall()
    column_names = [info['name'] for info in table_info]
    
    if 'widget_pos_x' not in column_names:
        cursor.execute('ALTER TABLE ips ADD COLUMN widget_pos_x INTEGER DEFAULT 100')
    if 'widget_pos_y' not in column_names:
        cursor.execute('ALTER TABLE ips ADD COLUMN widget_pos_y INTEGER DEFAULT 100')
    if 'widget_size' not in column_names:
        cursor.execute('ALTER TABLE ips ADD COLUMN widget_size TEXT DEFAULT "Medium"')
    if 'widget_ontop' not in column_names:
        cursor.execute('ALTER TABLE ips ADD COLUMN widget_ontop INTEGER DEFAULT 0')
        
    conn.commit()
    conn.close()

# --- All other functions are correct and unchanged ---
def get_all_ips():
    with get_db_connection() as conn: return conn.execute('SELECT * FROM ips ORDER BY address').fetchall()
def update_ip_widget_position(ip_id, x, y):
    with get_db_connection() as conn: conn.execute('UPDATE ips SET widget_pos_x = ?, widget_pos_y = ? WHERE id = ?', (x, y, ip_id))
def update_ip_widget_size(ip_id, size):
    with get_db_connection() as conn: conn.execute('UPDATE ips SET widget_size = ? WHERE id = ?', (size, ip_id))
def update_ip_widget_ontop(ip_id, on_top_status):
    with get_db_connection() as conn: conn.execute('UPDATE ips SET widget_ontop = ? WHERE id = ?', (on_top_status, ip_id))
def add_ip(address, description):
    with get_db_connection() as conn: conn.execute('INSERT OR IGNORE INTO ips (address, description) VALUES (?, ?)', (address, description))
def delete_ip(ip_id):
    with get_db_connection() as conn: conn.execute('DELETE FROM ips WHERE id = ?', (ip_id,))
def add_user(email):
    with get_db_connection() as conn: conn.execute('INSERT OR IGNORE INTO users (email) VALUES (?)', (email,))
def get_all_users():
    with get_db_connection() as conn: return conn.execute('SELECT * FROM users ORDER BY email').fetchall()
def delete_user(user_id):
    with get_db_connection() as conn: conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
def update_email_settings(sender_email, sender_password):
    with get_db_connection() as conn: conn.execute('UPDATE email_settings SET sender_email = ?, sender_password = ? WHERE id = 1', (sender_email, sender_password))
def get_email_settings():
    with get_db_connection() as conn: return conn.execute('SELECT * FROM email_settings WHERE id = 1').fetchone()

if __name__ == '__main__':
    initialize_db()
    print("Database schema updated successfully for final version.")