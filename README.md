# Flask Budget Tool

🌍 Languages: [English](#english) | [Deutsch](#deutsch)

---

## English

A lightweight weekly budget tool with customizable monthly cycle (start/end day), automatic weekly reset (Mondays), and carry-over from previous weeks.  
Developed & tested on Raspberry Pi (Debian-based OS, e.g. Raspberry Pi OS).  
Also works on other Linux systems with Python 3 and Flask installed.

⚠️ **Note:** Official support only for Debian-based systems.  
On Windows or macOS manual path adjustments/installation are required.

---

### Features
- Customizable monthly start/end day
- Automatic weekly reset (Mondays)
- Carry-over of leftover budgets into the new week
- Minimal resource usage – perfect for Raspberry Pi

---

### Installation (Raspberry Pi / Debian)

    # Update system & install Python environment
    sudo apt update && sudo apt install python3 python3-venv python3-pip -y

    # Clone repository
    git clone https://github.com/Python-XP1/flask-budget-tool.git
    cd flask-budget-tool

    # Create & activate virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt

    # Initialize database
    python3 init_db.py

---

### 🚀 Run the tool

`FLASK_SECRET_KEY` is required.

    # One-time for current shell session
    export FLASK_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"

    # Start app
    python3 app.py

Then open your browser and visit:  
- Local: http://localhost:5000  
- From another device in the same network: http://<IP_of_your_Pi/Pc>:5000  
  (example: http://192.168.178.25:5000)

Optional (persist in zsh):

    echo 'export FLASK_SECRET_KEY="your-long-random-key"' >> ~/.zshrc
    source ~/.zshrc

If you run the app via `systemd`, define the key in an environment file (for example `/etc/default/flask-budget-tool`).

---

### Extended Versions & Support 🚀
The published version here is the **free basic version**.

📦 **Pro versions** with additional features, bugfixes and early access updates are available exclusively for my **Patreon supporters**:  
👉 [Support Flask Budget Tool on Patreon](http://www.patreon.com/PythonXP)

By supporting, you help me continue developing this project and releasing new features regularly.

---

## Deutsch

Ein leichtgewichtiges Wochenbudget-Tool mit frei wählbarem Monatszyklus (Start-/Endtag), automatischem Wochen-Reset (montags) und Vorwochen-Übertrag.  
Entwickelt & getestet auf Raspberry Pi (Debian-basiertes OS, z. B. Raspberry Pi OS).  
Funktioniert auch auf anderen Linux-Systemen, wenn Python 3 und Flask installiert sind.

⚠️ **Hinweis:** Offizieller Support nur für Debian-basierte Systeme.  
Unter Windows oder macOS ist eine manuelle Anpassung der Pfade/Installation nötig.

---

### Features
- Frei wählbarer Monatsstart/-endtag
- Automatischer Wochenreset (montags)
- Übertrag von Restbudgets in die neue Woche
- Minimaler Ressourcenverbrauch – perfekt für Raspberry Pi

---

### Installation (Raspberry Pi / Debian)

    # System aktualisieren & Python-Umgebung bereitstellen
    sudo apt update && sudo apt install python3 python3-venv python3-pip -y

    # Repository klonen
    git clone https://github.com/Python-XP1/flask-budget-tool.git
    cd flask-budget-tool

    # Virtuelle Umgebung erstellen & aktivieren
    python3 -m venv venv
    source venv/bin/activate

    # Abhängigkeiten installieren
    pip install -r requirements.txt

    # Datenbank initialisieren
    python3 init_db.py

---

### 🚀 Tool starten

`FLASK_SECRET_KEY` ist erforderlich.

    # Einmalig für die aktuelle Shell-Session setzen
    export FLASK_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"

    # App starten
    python3 app.py

Dann den Browser öffnen und aufrufen:  
- Lokal: http://localhost:5000  
- Von einem anderen Gerät im selben Netzwerk: http://<IP_deines_Pi/Pc>:5000  
  (Beispiel: http://192.168.178.25:5000)

Optional (dauerhaft in zsh):

    echo 'export FLASK_SECRET_KEY="dein-langer-zufallsschluessel"' >> ~/.zshrc
    source ~/.zshrc

Wenn du über `systemd` startest, hinterlege den Key in einer Environment-Datei (z. B. `/etc/default/flask-budget-tool`).

---

### Erweiterte Versionen & Support 🚀
Die hier veröffentlichte Version ist die **kostenlose Basisversion**.

📦 **Pro-Versionen** mit zusätzlichen Features, Bugfixes und Early-Access-Updates gibt es exklusiv für meine **Patreon-Unterstützer**:  
👉 [Patreon – Flask Budget Tool unterstützen](http://www.patreon.com/PythonXP)

Mit deinem Support hilfst du mir, das Projekt weiterzuentwickeln und regelmäßig neue Funktionen bereitzustellen.
