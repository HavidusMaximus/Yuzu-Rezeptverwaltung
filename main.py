#######################################
# YUZU - Rezeptverwaltung
# Projektarbeit IHK Softwaredevelopment
# erstellt von Björn Brüner
#######################################


# Importe
import customtkinter as ctk
from tkinter import filedialog, Menu
from gui import fenster_rezept_hinzufuegen_dialog, fenster_rezept_suchen_dialog, show_info, zeige_impressum
from funktionsanweisungen import initialisiere_db, DB_PATH
import shutil


# Datenbank importieren bzw. Inhalte der zu importierenden Datenbank übernehmen
def datenbank_importieren_dialog(main_window):
    """
    Öffnet einen Dialog zum Importieren einer SQLite-Datenbank.
    Kopiert die ausgewählte Datenbankdatei in den festgelegten Pfad.
    """
    try:
        dateipfad = filedialog.askopenfilename(filetypes=[("SQLite-Datenbank", "*.db")], parent=main_window)
        if dateipfad:
            shutil.copyfile(dateipfad, DB_PATH)
            show_info(main_window, "Erfolg", "Datenbank erfolgreich importiert")
    except Exception as e:
        show_info(main_window, "Fehler", f"Fehler beim Importieren der Datenbank: {e}")

# Datenbank exportieren
def datenbank_exportieren_dialog(main_window):
    """
    Öffnet einen Dialog zum Exportieren der aktuellen SQLite-Datenbank.
    Speichert die Datenbankdatei am ausgewählten Ort.
    """
    try:
        dateipfad = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite-Datenbank", "*.db")], parent=main_window)
        if dateipfad:
            shutil.copyfile(DB_PATH, dateipfad)
            show_info(main_window, "Erfolg", "Datenbank erfolgreich exportiert")
    except Exception as e:
        show_info(main_window, "Fehler", f"Fehler beim Exportieren der Datenbank: {e}")

# Anwendung / Main initialisieren
def main():
    """
    Initialisiert die Anwendung, erstellt das Hauptfenster und fügt die GUI-Elemente hinzu.
    """
    initialisiere_db()

    fenster = ctk.CTk()
    fenster.title("Yuzu! Rezeptverwaltung")
    fenster.geometry("600x600")
    fenster.resizable(False, False)

    ctk.set_default_color_theme("green")

    # Menüleiste erstellen
    menubar = Menu(fenster)
    fenster.config(menu=menubar)

    datei_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Einstellungen", menu=datei_menu)
    datei_menu.add_command(label="Datenbank importieren", command=lambda: datenbank_importieren_dialog(fenster))
    datei_menu.add_command(label="Datenbank exportieren", command=lambda: datenbank_exportieren_dialog(fenster))
    datei_menu.add_command(label="Impressum", command=lambda: zeige_impressum(fenster))

    button_font = ('Calibri', 24, 'bold')

    fenster.columnconfigure(0, weight=1, uniform="column")
    fenster.columnconfigure(1, weight=1, uniform="column")
    fenster.rowconfigure(0, weight=1, uniform="row")
    fenster.rowconfigure(1, weight=1, uniform="row")

    button1 = ctk.CTkButton(fenster, text="Rezept suchen /\n anzeigen", font=button_font, command=lambda:
    fenster_rezept_suchen_dialog(fenster, "anzeigen"), height=100, width=200)
    button2 = ctk.CTkButton(fenster, text="Rezept hinzufügen", font=button_font, command=lambda:
    fenster_rezept_hinzufuegen_dialog(fenster, "Rezept hinzufügen"), height=100, width=200)
    button3 = ctk.CTkButton(fenster, text="Rezept editieren", font=button_font, command=lambda:
    fenster_rezept_suchen_dialog(fenster, "editieren"), height=100, width=200)
    button4 = ctk.CTkButton(fenster, text="Rezept löschen", font=button_font, command=lambda:
    fenster_rezept_suchen_dialog(fenster, "löschen"), height=100, width=200)

    button1.grid(row=0, column=0, padx=7, pady=7, sticky="nsew")
    button2.grid(row=0, column=1, padx=7, pady=7, sticky="nsew")
    button3.grid(row=1, column=0, padx=7, pady=7, sticky="nsew")
    button4.grid(row=1, column=1, padx=7, pady=7, sticky="nsew")

    fenster.mainloop()

if __name__ == "__main__":
    main()
