# Import
import sqlite3

# Datenbank festlegen
DB_PATH = "yuzu.db"

# Datenbank initialisieren / erstellen
def initialisiere_db():
    """
    Initialisiert die Datenbank und erstellt die notwendigen Tabellen.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS rezepte (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                zeitaufwand TEXT NOT NULL,
                zutaten TEXT NOT NULL,
                schritte TEXT NOT NULL,
                bild BLOB,
                erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                aktualisiert_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS kommentare (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rezept_id INTEGER NOT NULL,
                kommentar TEXT NOT NULL,
                erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rezept_id) REFERENCES rezepte (id) ON DELETE CASCADE
            )
            ''')
    except sqlite3.Error as e:
        print(f"Fehler bei der Initialisierung der Datenbank: {e}")

# Rezept zur Datenbank hinzufügen
def rezept_hinzufuegen(titel, zeitaufwand, zutaten, schritte, bild):
    """
    Fügt ein neues Rezept in die Datenbank ein.

    :param titel: Der Titel des Rezepts.
    :param zeitaufwand: Der Zeitaufwand für das Rezept.
    :param zutaten: Die Zutaten des Rezepts.
    :param schritte: Die Zubereitungsschritte des Rezepts.
    :param bild: Ein Bild des Rezepts.
    """
    if not titel:
        raise ValueError("Bitte gib mindestens einen Titel ein")

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO rezepte (titel, zeitaufwand, zutaten, schritte, bild)
            VALUES (?, ?, ?, ?, ?)
            ''', (titel, zeitaufwand, zutaten, schritte, bild))
    except sqlite3.Error as e:
        print(f"Fehler beim Hinzufügen des Rezepts: {e}")

# Rezept in Datenbank aktualisieren
def rezept_editieren(id, titel, zeitaufwand, zutaten, schritte, bild):
    """
    Aktualisiert ein bestehendes Rezept in der Datenbank.

    :param id: Die ID des Rezepts.
    :param titel: Der neue Titel des Rezepts.
    :param zeitaufwand: Der neue Zeitaufwand für das Rezept.
    :param zutaten: Die neuen Zutaten des Rezepts.
    :param schritte: Die neuen Zubereitungsschritte des Rezepts.
    :param bild: Das neue Bild des Rezepts.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            UPDATE rezepte
            SET titel = ?, zeitaufwand = ?, zutaten = ?, schritte = ?, bild = ?, aktualisiert_am = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (titel, zeitaufwand, zutaten, schritte, bild, id))
    except sqlite3.Error as e:
        print(f"Fehler beim Editieren des Rezepts: {e}")

# Rezept aus Datenbank löschen
def rezept_loeschen(id):
    """
    Löscht ein Rezept aus der Datenbank.

    :param id: Die ID des zu löschenden Rezepts.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            DELETE FROM rezepte WHERE id = ?
            ''', (id,))
    except sqlite3.Error as e:
        print(f"Fehler beim Löschen des Rezepts: {e}")

# Rezepte aus Datenbank anhand eines Suchbegriffes anzeigen
def rezepte_abrufen(suchbegriff):
    """
    Ruft Rezepte aus der Datenbank basierend auf einem Suchbegriff ab.

    :param suchbegriff: Der Suchbegriff für die Rezeptsuche.
    :return: Eine Liste der passenden Rezepte.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            SELECT id, titel FROM rezepte
            WHERE titel LIKE ?
            ORDER BY titel
            ''', ('%' + suchbegriff + '%',))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Fehler beim Abrufen der Rezepte: {e}")
        return []

# Einzelnes Rezept aus Datenbank anzeigen
def rezept_abrufen(id):
    """
    Ruft ein einzelnes Rezept aus der Datenbank ab.

    :param id: Die ID des Rezepts.
    :return: Das Rezept als Tupel.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            SELECT * FROM rezepte WHERE id = ?
            ''', (id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Fehler beim Abrufen des Rezepts: {e}")
        return None

# Kommentar zur Datenbank hinzufügen
def kommentar_hinzufuegen(rezept_id, kommentar):
    """
    Fügt einen neuen Kommentar zu einem Rezept hinzu.

    :param rezept_id: Die ID des Rezepts.
    :param kommentar: Der Kommentar.
    """
    if not kommentar:
        raise ValueError("Der Kommentar darf nicht leer sein.")

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO kommentare (rezept_id, kommentar)
            VALUES (?, ?)
            ''', (rezept_id, kommentar))
    except sqlite3.Error as e:
        print(f"Fehler beim Hinzufügen des Kommentars: {e}")

# Kommentar aus Datenbank aufrufen / anzeigen
def kommentare_abrufen(rezept_id):
    """
    Ruft alle Kommentare zu einem Rezept ab.

    :param rezept_id: Die ID des Rezepts.
    :return: Eine Liste der Kommentare.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
            SELECT id, kommentar, erstellt_am FROM kommentare
            WHERE rezept_id = ?
            ORDER BY erstellt_am DESC
            ''', (rezept_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Fehler beim Abrufen der Kommentare: {e}")
        return []
