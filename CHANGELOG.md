# 📜 Changelog – Flask Budget Tool

Alle nennenswerten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.  
Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/) und [Semantic Versioning](https://semver.org/).

All notable changes to this project will be documented in this file.  
The format is based on [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [Unreleased] – 2026-03-21

### Added
- [DE] CSRF-Schutz für alle mutierenden Requests (`POST`, `PUT`, `PATCH`, `DELETE`) inkl. Token in allen Formularen  
  [EN] CSRF protection for all mutating requests (`POST`, `PUT`, `PATCH`, `DELETE`) including tokens in all forms
- [DE] Pflichtdokumentation für `FLASK_SECRET_KEY` in der README (Shell und `systemd`)  
  [EN] Required `FLASK_SECRET_KEY` documentation added to README (shell and `systemd`)

### Changed
- [DE] App startet nicht mehr mit unsicherem Fallback-Secret, `FLASK_SECRET_KEY` ist jetzt verpflichtend  
  [EN] App no longer starts with an insecure fallback secret, `FLASK_SECRET_KEY` is now mandatory
- [DE] `init_db.py` nutzt jetzt ebenfalls `BUDGET_DB_PATH` für konsistente DB-Pfade  
  [EN] `init_db.py` now also uses `BUDGET_DB_PATH` for consistent DB paths

### Fixed
- [DE] `/clear-budgets` stabilisiert: `transfer_log` wird vor `DELETE` zuverlässig angelegt  
  [EN] Stabilized `/clear-budgets`: `transfer_log` is now ensured before `DELETE`

---

## [0.9.3] – 2025-08-17

### Added
- [DE] Mehrsprachigkeit (Deutsch & Englisch) mit Babel, `.po`- und `.mo`-Dateien  
  [EN] Multilanguage support (German & English) using Babel with `.po` and `.mo` files
- [DE] Neues Dropdown für Währungsauswahl (€, $, £ usw.)  
  [EN] New currency selection dropdown (€, $, £ etc.)
- [DE] Zweisprachiger Changelog für internationale Nutzer  
  [EN] Bilingual changelog for international users
- [DE] Ordnerstruktur optimiert: `instance/` für DB, `logs/` für Logs, `translations/` für Sprachdateien  
  [EN] Optimized folder structure: `instance/` for DB, `logs/` for logs, `translations/` for translations

### Changed
- [DE] Projektordner vereinheitlicht: `flask-budget-toolV0.9.3/` → `flask-budget-tool/`  
  [EN] Project folder unified: `flask-budget-toolV0.9.3/` → `flask-budget-tool/`
- [DE] Klare Trennung zwischen Code, Templates, Static Files und Daten  
  [EN] Clean separation between code, templates, static files, and data

### Fixed
- [DE] Übersetzungsprobleme bei Strings (z. B. „Betrag“, „Währung“) behoben  
  [EN] Fixed translation issues with some strings (e.g. "Amount", "Currency")
- [DE] Flash-Meldungen jetzt in beiden Sprachen korrekt  
  [EN] Flash messages now correctly translated in both languages
- [DE] Kleinere Layout-Inkonsistenzen gefixt  
  [EN] Fixed minor layout inconsistencies

---

## [0.9.2] – 2025-08-15 *(Patreon Exclusive)*

### Added
- [DE] Zentrierte Hauptüberschrift und Countdown für klarere Darstellung  
  [EN] Centered main header and countdown for clearer presentation
- [DE] Farb- und Stil-Optimierungen für bessere Lesbarkeit  
  [EN] Color and style optimizations for improved readability
- [DE] Einheitlicher Button-Style (Soft-Danger & Ghost-Buttons)  
  [EN] Unified button style (soft-danger & ghost buttons)
- [DE] Verbesserte Abstände und Layout für Komfort  
  [EN] Improved spacing and layout for usability

### Changed
- [DE] Farbschema verfeinert, Buttons & Warnungen konsistenter  
  [EN] Refined color scheme, buttons & alerts more consistent
- [DE] Wartungs- und Löschaktionen optisch hervorgehoben  
  [EN] Maintenance and delete actions visually emphasized

### Fixed
- [DE] Ausrichtung von Überschrift und Countdown korrigiert  
  [EN] Fixed alignment of header and countdown
- [DE] Kleinere CSS-Fehler behoben  
  [EN] Fixed minor CSS issues

---

## [0.9.0] – 2025-08-13

### Added
- [DE] Monatsbudget-Logik mit frei wählbarem Start- und Endtag  
  [EN] Monthly budget logic with freely selectable start and end date
- [DE] Wochenreset (montags) mit Vorwochen-Übertrag  
  [EN] Weekly reset (Mondays) with previous week carryover
- [DE] Weboberfläche mit Bootstrap-Design  
  [EN] Web interface with Bootstrap design
- [DE] Hilfsfunktionen ausgelagert in `utils/functions.py`  
  [EN] Utility functions outsourced to `utils/functions.py`
- [DE] `requirements.txt` für Setup hinzugefügt  
  [EN] `requirements.txt` added for easy setup
- [DE] Erste README.md & MIT-Lizenz hinzugefügt  
  [EN] First README.md & MIT license added

### Changed
- [DE] Code-Struktur in `app.py`, `init_db.py` und `utils/` verbessert  
  [EN] Improved code structure in `app.py`, `init_db.py`, and `utils/`
- [DE] Projektordner für GitHub-Release vorbereitet  
  [EN] Project folder prepared for GitHub release

### Fixed
- [DE] Bug bei Wochenstartberechnung behoben  
  [EN] Fixed bug in weekly reset calculation
- [DE] Fehlerhafte Anzeige beim Restbudget-Übertrag gefixt  
  [EN] Fixed incorrect display of budget carryover
