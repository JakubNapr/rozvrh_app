import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class PredmetyFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Název").pack()
        self.entry_nazev = tk.Entry(self)
        self.entry_nazev.pack()

        tk.Label(self, text="Zkratka").pack()
        self.entry_zkratka = tk.Entry(self)
        self.entry_zkratka.pack()

        tk.Button(self, text="Přidat", command=self.add_predmet).pack()

        self.tree = ttk.Treeview(self, columns=("ID", "Název", "Zkratka"), show="headings")
        for col in ("ID", "Název", "Zkratka"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        tk.Button(self, text="Smazat", command=self.delete_predmet).pack()

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM predmety")

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    def add_predmet(self):
        nazev = self.entry_nazev.get()
        zkratka = self.entry_zkratka.get()

        if not nazev or not zkratka:
            messagebox.showerror("Chyba", "Vyplň všechna pole")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO predmety (nazev, zkratka) VALUES (?, ?)", (nazev, zkratka))
        conn.commit()
        conn.close()

        self.entry_nazev.delete(0, tk.END)
        self.entry_zkratka.delete(0, tk.END)
        self.refresh()

    def delete_predmet(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        id = item["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predmety WHERE id=?", (id,))
        conn.commit()
        conn.close()

        self.refresh()
