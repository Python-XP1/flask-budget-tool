import sqlite3

conn = sqlite3.connect("budget.db")
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
    value REAL
)
""")

# Starttag initial eintragen, falls nicht vorhanden
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("start_day", 27))

# Endtag initial eintragen, falls nicht vorhanden
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("end_day", 26))

# Monatsbudget einmalig auf 0 setzen, falls nicht vorhanden
c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("monatsbudget", 0.0))

conn.commit()
conn.close()