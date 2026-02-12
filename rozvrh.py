import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


class RozvrhFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        #FORMULÁŘ 
        form_frame = ttk.LabelFrame(self, text="Přidat hodinu do rozvrhu", padding=10)
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Den:").grid(row=0, column=0, sticky="w", pady=2)
        self.combo_den = ttk.Combobox(
            form_frame,
            values=["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"],
            state="readonly"
        )
        self.combo_den.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(form_frame, text="Hodina:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_hodina = ttk.Entry(form_frame)
        self.entry_hodina.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(form_frame, text="Předmět:").grid(row=2, column=0, sticky="w", pady=2)
        self.combo_predmet = ttk.Combobox(form_frame, state="readonly")
        self.combo_predmet.grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Label(form_frame, text="Učitel:").grid(row=3, column=0, sticky="w", pady=2)
        self.combo_ucitel = ttk.Combobox(form_frame, state="readonly")
        self.combo_ucitel.grid(row=3, column=1, sticky="ew", pady=2)

        form_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=5)

        ttk.Button(btn_frame, text="Načíst data", command=self.load_comboboxes)\
            .pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Přidat do rozvrhu", command=self.add_rozvrh)\
            .pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Zobrazit rozvrh", command=self.refresh)\
            .pack(side="left", padx=5)

        #TREEVIEW
        table_frame = ttk.LabelFrame(self, text="Rozvrh", padding=5)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Den", "Hodina", "Předmět", "Učitel"),
            show="headings"
        )

        for col in ("ID", "Den", "Hodina", "Předmět", "Učitel"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Den", width=100, anchor="center")
        self.tree.column("Hodina", width=80, anchor="center")
        self.tree.column("Předmět", anchor="w")
        self.tree.column("Učitel", anchor="w")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        #SMAZAT
        ttk.Button(self, text="Smazat vybranou hodinu", command=self.delete_rozvrh)\
            .pack(pady=5)

        #INIT
        self.combo_den.current(0)
        self.load_comboboxes()
        self.refresh()

    def load_comboboxes(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT nazev FROM predmety")
        self.combo_predmet["values"] = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT jmeno FROM ucitele")
        self.combo_ucitel["values"] = [row[0] for row in cursor.fetchall()]

        conn.close()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        den = self.combo_den.get()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT rozvrh.id, rozvrh.den, rozvrh.hodina,
                   predmety.nazev, ucitele.jmeno
            FROM rozvrh
            JOIN predmety ON rozvrh.predmet_id = predmety.id
            JOIN ucitele ON rozvrh.ucitel_id = ucitele.id
            WHERE rozvrh.den=?
        """, (den,))

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    def add_rozvrh(self):
        den = self.combo_den.get()
        hodina = self.entry_hodina.get()
        predmet = self.combo_predmet.get()
        ucitel = self.combo_ucitel.get()

        if not den or not hodina or not predmet or not ucitel:
            messagebox.showerror("Chyba", "Vyplň všechna pole")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM predmety WHERE nazev=?", (predmet,))
        predmet_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM ucitele WHERE jmeno=?", (ucitel,))
        ucitel_id = cursor.fetchone()[0]

        cursor.execute("""
            SELECT * FROM rozvrh
            WHERE den=? AND hodina=? AND ucitel_id=?
        """, (den, hodina, ucitel_id))

        if cursor.fetchone():
            messagebox.showerror("Chyba", "Učitel už má v tuto dobu hodinu")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO rozvrh (den, hodina, predmet_id, ucitel_id)
            VALUES (?, ?, ?, ?)
        """, (den, hodina, predmet_id, ucitel_id))

        conn.commit()
        conn.close()
        self.refresh()

    def delete_rozvrh(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber hodinu ke smazání")
            return

        item = self.tree.item(selected[0])
        rozvrh_id = item["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rozvrh WHERE id=?", (rozvrh_id,))
        conn.commit()
        conn.close()

        self.refresh()

