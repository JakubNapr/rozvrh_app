import sqlite3

def get_connection():
    return sqlite3.connect("rozvrh.db")

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predmety (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazev TEXT NOT NULL,
        zkratka TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ucitele (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jmeno TEXT NOT NULL,
        kabinet TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rozvrh (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        den TEXT NOT NULL,
        hodina INTEGER NOT NULL,
        predmet_id INTEGER,
        ucitel_id INTEGER,
        FOREIGN KEY (predmet_id) REFERENCES predmety(id),
        FOREIGN KEY (ucitel_id) REFERENCES ucitele(id)
    )
    """)

    conn.commit()
    conn.close()
