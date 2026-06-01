import sqlite3

def init():
    conn = sqlite3.connect('file_sharing.db')
    cursor = conn.cursor()
    # Menambah kolom metadata biar makin pro
    cursor.execute('''CREATE TABLE IF NOT EXISTS files 
                      (kode TEXT, file_id TEXT, uploader_id INTEGER, timestamp DATETIME)''')
    conn.commit()
    conn.close()

def run(query, params=()):
    conn = sqlite3.connect('file_sharing.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data
