import os
import sqlite3

DB_PATH = os.environ.get("BUDGET_DB_PATH", "budget.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Tabelle für Ausgaben
c.execute("""
CREATE TABLE IF NOT EXISTS ausgaben (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datum TEXT NOT NULL,
    betrag REAL NOT NULL,
    beschreibung TEXT
)
""")

# Tabelle für Einstellungen (z. B. Monatsbudget, Start- und Endtag)
c.execute("""
CREATE TABLE IF NOT EXISTS einstellungen (
    key TEXT PRIMARY KEY,
    value
)
""")

# Tabelle für Wochenübertrag-Tracking
c.execute("""
CREATE TABLE IF NOT EXISTS transfer_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start TEXT NOT NULL UNIQUE,
    transferred INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Grundeinstellungen initial eintragen, falls nicht vorhanden
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("start_day", 27))
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("end_day", 26))
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("monatsbudget", 0.0))
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("activated_at", None))
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("currency", "EUR"))

conn.commit()
conn.close()
