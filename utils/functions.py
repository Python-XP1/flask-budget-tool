# functions.py
import sqlite3
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar
import os

# -----------------------------
# DB / Settings Basis
# -----------------------------
DB_PATH = os.environ.get("BUDGET_DB_PATH", "budget.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_setting(key: str, default=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM einstellungen WHERE key=?", (key,))
    row = cur.fetchone()
    conn.close()
    if row is None or row[0] is None:
        return default
    return row[0]

def set_setting(key: str, value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO einstellungen (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def ensure_settings():
    """
    Legt fehlende Einstellungen an, ohne vorhandene zu überschreiben.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("start_day", 27))
    c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("end_day", 26))
    c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("monatsbudget", 0.0))
    c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("activated_at", None))
    c.execute("INSERT OR IGNORE INTO einstellungen (key, value) VALUES (?, ?)", ("currency", "EUR"))
    conn.commit()
    conn.close()

# -----------------------------
# Währung / Currency
# -----------------------------
# (ISO, Symbol)
_CURRENCY_CHOICES = [
    ("EUR", "€"),
    ("USD", "$"),
    ("GBP", "£"),
    ("CHF", "CHF"),
    ("PLN", "zł"),
    ("SEK", "kr"),
    ("NOK", "kr"),
    ("DKK", "kr"),
    ("JPY", "¥"),
    ("CNY", "¥"),
    ("INR", "₹"),
]

def get_currency_choices() -> list[tuple[str, str]]:
    """Liste der erlaubten Währungen (ISO, Symbol)."""
    return _CURRENCY_CHOICES

def get_currency_symbol(default: str = "€") -> str:
    """Hole das aktuell gesetzte Symbol aus den Einstellungen (Fallback €)."""
    val = get_setting("currency", None)
    if not val:
        return default
    # val kann ISO oder Symbol sein – mappe sicher auf Symbol
    for iso, sym in _CURRENCY_CHOICES:
        if val == iso or val == sym:
            return sym
    return default

# -----------------------------
# Datum/Zyklus
# -----------------------------
def month_last_day(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]

def safe_date(year: int, month: int, day: int) -> date:
    return date(year, month, min(day, month_last_day(year, month)))

def get_end_day() -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM einstellungen WHERE key = 'end_day'")
    row = cur.fetchone()
    conn.close()
    return int(row[0]) if row and row[0] is not None else 26

def get_start_day() -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM einstellungen WHERE key = 'start_day'")
    row = cur.fetchone()
    conn.close()
    return int(row[0]) if row and row[0] is not None else 27

def get_cycle_for_date(ref: date, start_day: int, end_day: int) -> tuple[date, date]:
    # Start
    if ref.day < start_day:
        s_year, s_month = (ref.year - 1, 12) if ref.month == 1 else (ref.year, ref.month - 1)
    else:
        s_year, s_month = ref.year, ref.month
    zyklus_start = safe_date(s_year, s_month, start_day)

    # Ende
    if end_day > start_day:
        e_year, e_month = s_year, s_month
        zyklus_ende = safe_date(e_year, e_month, end_day)
    elif end_day < start_day:
        e_year, e_month = (s_year + 1, 1) if s_month == 12 else (s_year, s_month + 1)
        zyklus_ende = safe_date(e_year, e_month, end_day)
    else:
        # Stichtags-Modus (gleicher Tag) -> bis Vortag des nächsten Monats-Stichtags
        e_year, e_month = (s_year + 1, 1) if s_month == 12 else (s_year, s_month + 1)
        zyklus_ende = safe_date(e_year, e_month, end_day) - timedelta(days=1)

    # Schutz
    if zyklus_ende < zyklus_start:
        e_year, e_month = (e_year + 1, 1) if e_month == 12 else (e_year, e_month + 1)
        zyklus_ende = safe_date(e_year, e_month, end_day)

    return zyklus_start, zyklus_ende

def overlap_days(a_start: date, a_end: date, b_start: date, b_end: date) -> int:
    start = max(a_start, b_start)
    end = min(a_end, b_end)
    if end < start:
        return 0
    return (end - start).days + 1

def get_current_week() -> tuple[date, date]:
    today = date.today()
    start = today - timedelta(days=today.weekday())  # Montag
    end = start + timedelta(days=6)                  # Sonntag
    return start, end

def is_valid_cycle(start_day: int, end_day: int) -> bool:
    # mind. 7 Tage
    if end_day >= start_day:
        return (end_day - start_day + 1) >= 7
    else:
        return ((31 - start_day + 1) + end_day) >= 7

def get_current_month_range() -> tuple[str, str]:
    start_day = get_start_day()
    end_day = get_end_day()
    zyklus_start, zyklus_ende = get_cycle_for_date(date.today(), start_day, end_day)
    return zyklus_start.strftime("%d.%m."), zyklus_ende.strftime("%d.%m.")

def get_next_monday() -> datetime:
    today = datetime.now()
    days_ahead = 0 - today.weekday()  # Montag=0
    if days_ahead <= 0:
        days_ahead += 7
    next_monday = today + timedelta(days=days_ahead)
    return next_monday.replace(hour=0, minute=0, second=0, microsecond=0)

def get_monetary_cycle():
    # legacy helper
    today = datetime.today().date()
    if today.day >= 27:
        start = today.replace(day=27)
        end = (start + relativedelta(months=1)).replace(day=26)
    else:
        end = today.replace(day=26)
        start = (end - relativedelta(months=1)).replace(day=27)
    return start, end

# -----------------------------
# Aktivierung & Übertrag-Logik
# -----------------------------
def first_monday_after(d: date) -> date:
    shift = (7 - d.weekday()) % 7
    if shift == 0:
        shift = 7
    return d + timedelta(days=shift)

def activated_date():
    val = get_setting("activated_at", None)
    if not val:
        return None
    return datetime.strptime(str(val), "%Y-%m-%d").date()

def current_week_start(d: date | None = None) -> date:
    if d is None:
        d = date.today()
    return d - timedelta(days=d.weekday())

def activated_this_week() -> bool:
    a = activated_date()
    if not a:
        return False
    return a >= current_week_start()

def is_transfer_active(today: date) -> bool:
    val = get_setting("activated_at", None)
    if not val:
        return False
    try:
        activated = datetime.strptime(val, "%Y-%m-%d").date()
    except Exception:
        return False
    return today >= first_monday_after(activated)

def get_current_monday() -> str:
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    return monday.strftime("%Y-%m-%d")

def ensure_transfer_tracking_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transfer_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start TEXT NOT NULL UNIQUE,
            transferred INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def has_transferred_for_week() -> bool:
    monday = get_current_monday()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT transferred FROM transfer_log WHERE week_start = ?", (monday,))
    result = c.fetchone()
    conn.close()
    return bool(result and result[0] == 1)

def mark_week_as_transferred():
    monday = get_current_monday()
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO transfer_log (week_start, transferred) VALUES (?, 1)", (monday,))
    conn.commit()
    conn.close()

def reset_wochenbudget():
    restbetrag = get_last_week_balance()
    print(f"Übertrag aus letzter Woche: {restbetrag:.2f} €")

def guarded_wochenuebertrag():
    if activated_this_week():
        print("⏭️  Übertrag übersprungen: Aktivierung in dieser Woche.")
        return
    ensure_transfer_tracking_table()
    if not is_transfer_active(date.today()):
        return
    if not has_transferred_for_week():
        print("🔁 Übertrag wird durchgeführt...")
        reset_wochenbudget()
        mark_week_as_transferred()
    else:
        print("✅ Übertrag für diese Woche wurde bereits gemacht.")

def get_last_transfer_date():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT week_start FROM transfer_log
        WHERE transferred = 1
        ORDER BY week_start DESC
        LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_last_week_balance() -> float:
    current_start, current_end = get_current_week()
    last_week_start = current_start - timedelta(days=7)
    last_week_end   = current_end   - timedelta(days=7)

    conn = get_connection()
    c = conn.cursor()

    # Budget
    c.execute("SELECT value FROM einstellungen WHERE key='monatsbudget'")
    row = c.fetchone()
    monatsbudget = float(row[0]) if row and row[0] is not None else 0.0

    # Start/Endtag
    start_day = get_start_day()
    end_day = get_end_day()

    # Zyklus -> Wochenbudget
    zyklus_start, zyklus_ende = get_cycle_for_date(date.today(), start_day, end_day)
    tage_gesamt = (zyklus_ende - zyklus_start).days + 1
    tagesbudget = monatsbudget / tage_gesamt if tage_gesamt > 0 else 0.0
    wochenbudget = round(tagesbudget * 7, 2)

    # Ausgaben Vorwoche
    c.execute("""
        SELECT SUM(betrag) FROM ausgaben
        WHERE date(datum) BETWEEN ? AND ?
    """, (last_week_start.isoformat(), last_week_end.isoformat()))
    row = c.fetchone()
    summe = float(row[0]) if row and row[0] is not None else 0.0
    ausgaben = abs(summe)

    conn.close()
    return round(wochenbudget - ausgaben, 2)

# -----------------------------
# Mehrsprachigkeit / i18n
# -----------------------------

# unterstützte Sprachen
LANGUAGES = ["de", "en"]

def get_supported_languages() -> list[str]:
    return LANGUAGES

def get_default_locale() -> str:
    return "de"

def get_default_timezone() -> str:
    return "Europe/Berlin"

def resolve_locale(request, session) -> str:
    """
    Ermittelt die aktuelle Sprache nach Priorität:
    1. Query param ?lang=de|en (setzt Session)
    2. Session["lang"]
    3. Accept-Language Header (best_match)
    """
    lang_qp = request.args.get("lang")
    if lang_qp in LANGUAGES:
        session["lang"] = lang_qp
        return lang_qp
    if "lang" in session and session["lang"] in LANGUAGES:
        return session["lang"]
    return request.accept_languages.best_match(LANGUAGES) or get_default_locale()