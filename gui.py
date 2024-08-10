# Importe 
import customtkinter as ctk
from tkinter import ttk, filedialog
from PIL import Image
from funktionsanweisungen import rezept_hinzufuegen, rezept_editieren, rezept_loeschen, rezepte_abrufen, rezept_abrufen, \
    kommentar_hinzufuegen, kommentare_abrufen
import io

# Konstanten für Farben und Stile
BG_COLOR = "#333333"
FG_COLOR = "white"
SELECTED_COLOR = "#1a73e8"

# Fenster in den Vordergrund bringen
def bring_to_front(window):
    """
    Bringt das angegebene Fenster in den Vordergrund.

    :param window: Das Fenster, das in den Vordergrund gebracht werden soll.
    """
    window.lift()
    window.attributes('-topmost', True)
    window.after(200, lambda: window.attributes('-topmost', False))

# Fenster-Toggle / Minimieren
def toggle_window(current_window, new_window):
    """
    Blendet das aktuelle Fenster aus und zeigt das neue Fenster an.

    :param current_window: Das aktuelle Fenster, das ausgeblendet werden soll.
    :param new_window: Das neue Fenster, das angezeigt werden soll.
    """
    current_window.withdraw()
    new_window.deiconify()
    bring_to_front(new_window)


# Message-Box mit OK-Button
def show_info(parent, title, message):
    """
    Zeigt eine Messagebox mit einem OK-Button an.

    :param parent: Das übergeordnete Fenster.
    :param title: Der Titel der Messagebox.
    :param message: Die Nachricht, die in der Messagebox angezeigt wird.
    """
    box = ctk.CTkToplevel(parent)
    box.title(title)
    box.geometry("300x150")
    box.resizable(False, False)
    box.attributes('-topmost', True)

    label_message = ctk.CTkLabel(box, text=message)
    label_message.pack(pady=20, padx=20)

    button_frame = ctk.CTkFrame(box)
    button_frame.pack(pady=10)

    result = None

    # Event bei Button-Klick
    def _on_button_click():
        nonlocal result
        result = True
        box.destroy()

    button = ctk.CTkButton(button_frame, text="OK", command=_on_button_click)
    button.pack(side="left", padx=10)

    box.grab_set()
    box.wait_window()
    return result


# Message-Box mit Ja/Nein-Buttons
def ask_yes_no(parent, title, message):
    """
    Zeigt eine Messagebox mit Ja- und Nein-Buttons an.

    :param parent: Das übergeordnete Fenster.
    :param title: Der Titel der Messagebox.
    :param message: Die Nachricht, die in der Messagebox angezeigt wird.
    :return: True, wenn "Ja" gedrückt wird, sonst False.
    """
    box = ctk.CTkToplevel(parent)
    box.title(title)
    box.geometry("300x150")
    box.resizable(False, False)
    box.attributes('-topmost', True)

    label_message = ctk.CTkLabel(box, text=message)
    label_message.pack(pady=20, padx=20)

    button_frame = ctk.CTkFrame(box)
    button_frame.pack(pady=10)

    result = None

    # Event bei Button-Klick
    def _on_button_click(value):
        nonlocal result
        result = value
        box.destroy()

    button_yes = ctk.CTkButton(button_frame, text="Ja", command=lambda: _on_button_click(True))
    button_yes.pack(side="left", padx=10)

    button_no = ctk.CTkButton(button_frame, text="Nein", command=lambda: _on_button_click(False))
    button_no.pack(side="left", padx=10)

    box.grab_set()
    box.wait_window()
    return result

# Fenster für das Hinzufügen / Bearbeiten eines Rezeptes
def fenster_rezept_hinzufuegen_dialog(parent, titel, rezept=None, editierbar=True):
    """
    Öffnet ein Fenster zum Hinzufügen oder Bearbeiten eines Rezepts.

    :param parent: Das übergeordnete Fenster.
    :param titel: Der Titel des Fensters.
    :param rezept: Das Rezept, das bearbeitet werden soll (optional).
    :param editierbar: Ob das Rezept bearbeitet werden kann.
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title(titel)
    dialog.geometry("700x700")
    dialog.resizable(False, False)
    bring_to_front(dialog)
    toggle_window(parent, dialog)

    # Event bei Close
    def on_close():
        dialog.destroy()
        parent.deiconify()

    dialog.protocol("WM_DELETE_WINDOW", on_close)

    # Variable für das Bild deklarieren
    bild_blob = [None]

    # Dialog für das Auswählen und Laden eines Bildes
    def bild_durchsuchen():
        """
        Öffnet einen Dialog zum Auswählen eines Bildes und lädt das Bild.
        """
        dateipfad = filedialog.askopenfilename(parent=dialog, filetypes=[("Bilddateien", "*.jpg;*.jpeg;*.png")])
        if dateipfad:
            with open(dateipfad, 'rb') as file:
                bild_blob[0] = file.read()
            bild = Image.open(io.BytesIO(bild_blob[0]))
            bild = bild.resize((200, 200))
            bild_ctk = ctk.CTkImage(light_image=bild, size=(200, 200))
            label_bild.configure(image=bild_ctk, text="")
            label_bild.image = bild_ctk

    label_titel = ctk.CTkLabel(dialog, text="Titel")
    label_titel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_titel = ctk.CTkEntry(dialog)
    entry_titel.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    label_zeitaufwand = ctk.CTkLabel(dialog, text="Zeitaufwand\n(in Minuten)")
    label_zeitaufwand.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    entry_zeitaufwand = ctk.CTkEntry(dialog)
    entry_zeitaufwand.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    label_zutaten = ctk.CTkLabel(dialog, text="Zutaten")
    label_zutaten.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    text_zutaten = ctk.CTkTextbox(dialog, height=100)
    text_zutaten.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    label_bild = ctk.CTkLabel(dialog, text="Bild", width=200, height=200, fg_color="grey")
    label_bild.grid(row=0, column=2, rowspan=3, padx=10, pady=10, sticky="ns")

    if editierbar:
        button_bild_durchsuchen = ctk.CTkButton(dialog, text="Durchsuchen...", command=bild_durchsuchen)
        button_bild_durchsuchen.grid(row=3, column=2, padx=10, pady=(0, 10), sticky="ew")

    label_schritte_groß = ctk.CTkLabel(dialog, text="Schritte")
    label_schritte_groß.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    text_schritte = ctk.CTkTextbox(dialog, height=300)
    text_schritte.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

    if rezept and len(rezept) >= 6:
        entry_titel.insert(0, rezept[1])
        entry_zeitaufwand.insert(0, rezept[2])
        text_zutaten.insert("1.0", rezept[3])
        text_schritte.insert("1.0", rezept[4])
        if rezept[5] and isinstance(rezept[5], bytes):
            bild = Image.open(io.BytesIO(rezept[5]))
            bild = bild.resize((200, 200), Image.LANCZOS)
            bild_ctk = ctk.CTkImage(light_image=bild, size=(200, 200))
            label_bild.configure(image=bild_ctk, text="")
            label_bild.image = bild_ctk
            bild_blob[0] = rezept[5]

    if not editierbar:
        entry_titel.configure(state="disabled")
        entry_zeitaufwand.configure(state="disabled")
        text_zutaten.configure(state="disabled")
        text_schritte.configure(state="disabled")

    button_frame = ctk.CTkFrame(dialog)
    button_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="e")

    # Event bei Button-Klick
    def zurück():
        dialog.destroy()
        parent.deiconify()

    zurück_button = ctk.CTkButton(button_frame, text="Zurück", command=zurück)
    zurück_button.pack(side="left", padx=10)

    if editierbar:
        speichern_button = ctk.CTkButton(button_frame, text="Speichern",
                                         command=lambda: speichern_rezept(rezept[0] if rezept else None,
                                                                          entry_titel.get(),
                                                                          entry_zeitaufwand.get(),
                                                                          text_zutaten.get("1.0", "end-1c"),
                                                                          text_schritte.get("1.0", "end-1c"),
                                                                          bild_blob[0],
                                                                          dialog))
        speichern_button.pack(side="left", padx=10)
    else:
        kommentare_button = ctk.CTkButton(button_frame, text="Kommentare",
                                          command=lambda: fenster_kommentare(dialog, rezept[0]))
        kommentare_button.pack(side="left", padx=10)

# Rezept speichern / aktualisieren und in der Datenbank speichern
def speichern_rezept(rezept_id, titel, zeitaufwand, zutaten, schritte, bild_blob, fenster):
    """
    Speichert ein neues oder aktualisiertes Rezept in der Datenbank.

    :param rezept_id: Die ID des Rezepts (oder None für ein neues Rezept).
    :param titel: Der Titel des Rezepts.
    :param zeitaufwand: Der Zeitaufwand für das Rezept.
    :param zutaten: Die Zutaten des Rezepts.
    :param schritte: Die Zubereitungsschritte des Rezepts.
    :param bild_blob: Das Bild des Rezepts als Blob.
    :param fenster: Das Fenster, das nach dem Speichern geschlossen wird.
    """
    try:
        if not titel.strip():
            show_info(fenster, "Fehler", "Der Titel darf nicht leer sein!")
            return

        if rezept_id:
            rezept_editieren(rezept_id, titel, zeitaufwand, zutaten, schritte, bild_blob)
        else:
            rezept_hinzufuegen(titel, zeitaufwand, zutaten, schritte, bild_blob)
        show_info(fenster, "Erfolg", "Rezept erfolgreich gespeichert")
        fenster.destroy()
        fenster.master.deiconify()
    except ValueError as e:
        show_info(fenster, "Fehler", str(e))

# Fenster für die Anzeige und das Hinzufügen von Kommentaren
def fenster_kommentare(parent, rezept_id):
    """
    Öffnet ein Fenster zur Anzeige und Hinzufügung von Kommentaren zu einem Rezept.

    :param parent: Das übergeordnete Fenster.
    :param rezept_id: Die ID des Rezepts.
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Kommentare")
    dialog.geometry("600x600")
    dialog.resizable(False, False)
    bring_to_front(dialog)
    toggle_window(parent, dialog)

    # Event bei Close
    def on_close():
        dialog.destroy()
        parent.deiconify()

    dialog.protocol("WM_DELETE_WINDOW", on_close)
    # Kommentar hinzufügen
    def kommentar_hinzufuegen_handler():
        """
        Event-Handler zum Hinzufügen eines neuen Kommentars.
        """
        kommentar_text = kommentar_entry.get("1.0", "end-1c")
        try:
            if kommentar_text:
                kommentar_hinzufuegen(rezept_id, kommentar_text)
                kommentar_entry.delete("1.0", "end")
                suchen()
        except ValueError as e:
            show_info(dialog, "Fehler", str(e))

    kommentar_frame = ctk.CTkFrame(dialog)
    kommentar_frame.pack(pady=10, padx=10, fill="x")

    kommentar_label = ctk.CTkLabel(kommentar_frame, text="Neuen Kommentar hinzufügen:")
    kommentar_label.pack(anchor="w")

    kommentar_entry = ctk.CTkTextbox(kommentar_frame, height=100)
    kommentar_entry.pack(fill="x", pady=5)

    kommentar_button = ctk.CTkButton(kommentar_frame, text="Hinzufügen", command=kommentar_hinzufuegen_handler)
    kommentar_button.pack(pady=5)

    tree_frame = ctk.CTkFrame(dialog)
    tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

    columns = ("ID", "Kommentar", "Erstellt am")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.heading("ID", text="ID", anchor="w")
    tree.heading("Kommentar", text="Kommentar", anchor="w")
    tree.heading("Erstellt am", text="Erstellt am", anchor="w")
    tree.column("ID", width=50, anchor="w")
    tree.column("Kommentar", width=300, anchor="w")
    tree.column("Erstellt am", width=150, anchor="w")
    tree.pack(fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=BG_COLOR, foreground=FG_COLOR, fieldbackground=BG_COLOR, rowheight=25, bordercolor=BG_COLOR, borderwidth=0)
    style.configure("Treeview.Heading", background="#3a3a3a", foreground=FG_COLOR, bordercolor="#3a3a3a", borderwidth=1, relief="flat", font=("Calibri", 12, "bold"), anchor="w")
    style.map("Treeview", background=[("selected", SELECTED_COLOR)])
    style.map("Treeview.Heading", background=[("selected", "#3a3a3a")])
    # Kommentare suchen und (alle) zeigen
    def suchen():
        """
        Sucht und zeigt alle Kommentare zu dem Rezept an.
        """
        kommentare = kommentare_abrufen(rezept_id)
        for item in tree.get_children():
            tree.delete(item)
        for kommentar in kommentare:
            tree.insert("", "end", values=(kommentar[0], kommentar[1], kommentar[2]))

    suchen()
    # Event bei Button-Klick
    def zurück():
        dialog.destroy()
        parent.deiconify()

    zurück_button = ctk.CTkButton(dialog, text="Zurück", command=zurück)
    zurück_button.pack(pady=10)

# Message-Box mit Löschbestätigung anzeigen / Rezept löschen
def confirm_delete(rezept_id, parent, such_funktion):
    """
    Zeigt eine Bestätigungs-Messagebox zum Löschen eines Rezepts an und löscht das Rezept bei Bestätigung.

    :param rezept_id: Die ID des zu löschenden Rezepts.
    :param parent: Das übergeordnete Fenster.
    :param such_funktion: Die Suchfunktion, die nach dem Löschen aufgerufen wird.
    """
    result = ask_yes_no(parent, "Löschen bestätigen", "Möchtest du dieses Rezept wirklich löschen?")
    if result:
        rezept_loeschen(rezept_id)
        show_info(parent, "Erfolg", "Rezept erfolgreich gelöscht")
        such_funktion()

# Fenster für die Suche und Auswahl eines Rezeptes
def fenster_rezept_suchen_dialog(parent, zweck):
    """
    Öffnet ein Fenster zum Suchen und Auswählen eines Rezepts.

    :param parent: Das übergeordnete Fenster.
    :param zweck: Der Zweck des Suchfensters (löschen, anzeigen, editieren).
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Rezept suchen / anzeigen")
    dialog.geometry("600x600")
    dialog.resizable(False, False)
    bring_to_front(dialog)
    toggle_window(parent, dialog)
    selected_rezept = [None]

    # Event bei Close
    def on_close():
        dialog.destroy()
        parent.deiconify()

    dialog.protocol("WM_DELETE_WINDOW", on_close)
    # Echtzeit-Suche eines Suchbegriffes
    def suchen(*args):
        """
        Sucht Rezepte basierend auf dem eingegebenen Suchbegriff in Echtzeit.
        """
        suchbegriff = search_entry.get()
        rezepte = rezepte_abrufen(suchbegriff)
        for item in tree.get_children():
            tree.delete(item)
        for rezept in rezepte:
            tree.insert("", "end", values=(rezept[0], rezept[1]))
    # Rezept auswählen
    def rezept_auswaehlen(event):
        """
        Event-Handler für die Auswahl eines Rezepts aus der Liste.
        """
        selected_item = tree.focus()
        if selected_item:
            selected_rezept[0] = tree.item(selected_item)["values"]

    search_frame = ctk.CTkFrame(dialog)
    search_frame.pack(pady=10, padx=10, fill="x")

    search_entry = ctk.CTkEntry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    search_entry.bind("<KeyRelease>", suchen)

    search_button = ctk.CTkButton(search_frame, text="Suchen", command=suchen)
    search_button.pack(side="left")

    tree_frame = ctk.CTkFrame(dialog)
    tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

    columns = ("ID", "Rezeptname")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.heading("ID", text="ID", anchor="w")
    tree.heading("Rezeptname", text="Rezeptname", anchor="w")
    tree.column("ID", width=50, anchor="w")
    tree.column("Rezeptname", width=150, anchor="w")
    tree.pack(fill="both", expand=True)

    tree.bind("<<TreeviewSelect>>", rezept_auswaehlen)

    button_frame = ctk.CTkFrame(dialog)
    button_frame.pack(pady=10)

    if zweck == "löschen":
        action_button = ctk.CTkButton(button_frame, text="Löschen",
                                      command=lambda: confirm_delete(selected_rezept[0][0], dialog, suchen) if
                                      selected_rezept[0] else None)
    elif zweck == "anzeigen":
        action_button = ctk.CTkButton(button_frame, text="Rezept anzeigen",
                                      command=lambda: fenster_rezept_hinzufuegen_dialog(dialog, "Rezept anzeigen",
                                                                                 rezept_abrufen(selected_rezept[0][0]),
                                                                                 False) if selected_rezept[0] else None)
    elif zweck == "editieren":
        action_button = ctk.CTkButton(button_frame, text="Editieren",
                                      command=lambda: fenster_rezept_hinzufuegen_dialog(dialog, "Rezept editieren",
                                                                                 rezept_abrufen(
                                                                                     selected_rezept[0][0])) if
                                      selected_rezept[0] else None)

    action_button.pack(pady=10)

    # Event bei Button-Klick
    def zurück():
        dialog.destroy()
        parent.deiconify()

    zurück_button = ctk.CTkButton(dialog, text="Zurück", command=zurück)
    zurück_button.pack(pady=10)

    suchen()

# Impressum anzeigen
def zeige_impressum(parent):
    """
    Zeigt ein Fenster mit einem Beispielimpressum an.

    :param parent: Das übergeordnete Fenster.
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Impressum")
    dialog.geometry("400x300")
    dialog.resizable(False, False)
    bring_to_front(dialog)

    label_impressum = ctk.CTkLabel(dialog, text="Impressum\n\n\n\n\n"
                                                "Yuzu! Rezeptverwaltung\n\n\n"
                                                "Idee und Entwicklung:\n\n\n"
                                                "Björn Brüner\n"
                                                )
    label_impressum.pack(pady=20, padx=20)

    button_ok = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
    button_ok.pack(pady=10)
