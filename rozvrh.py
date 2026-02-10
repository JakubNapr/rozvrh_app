import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class RozvrhFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Den").pack()
        self.combo_den = ttk.Combobox(self, values=["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"])
        self.combo_den.pack()

        tk.Label(self, text="Hodina").pack()
        self.entry_hodina = tk.Entry(self)
        self.entry_hodina.pack()

        tk.Label(self, text="Předmět").pack()
        self.combo_predmet = ttk.Combobox(self)
        self.combo_predmet.pack()

        tk.Label(self, text="Učitel").pack()
        self.combo_ucitel = ttk.Combobox(self)
        self.combo_ucitel.pack()

        tk.Button(self, text="Načíst data", command=self.load_comboboxes).pack()
        tk.Button(self, text="Přidat do rozvrhu", command=self.add_rozvrh).pack()
        tk.Button(self, text="Zobrazit rozvrh", command=self.refresh).pack()

        self.tree = ttk.Treeview(self,
                                 columns=("ID", "Den", "Hodina", "Předmět", "Učitel"),
                                 show="headings")

        for col in ("ID", "Den", "Hodina", "Předmět", "Učitel"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

        tk.Button(self, text="Smazat hodinu", command=self.delete_rozvrh).pack()

        self.combo_den.current(0)   # výchozí den = Pondělí
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
            return

        item = self.tree.item(selected[0])
        id = item["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rozvrh WHERE id=?", (id,))
        conn.commit()
        conn.close()

        self.refresh()
