import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class UciteleFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Jméno").pack()
        self.entry_jmeno = tk.Entry(self)
        self.entry_jmeno.pack()

        tk.Label(self, text="Kabinet").pack()
        self.entry_kabinet = tk.Entry(self)
        self.entry_kabinet.pack()

        tk.Button(self, text="Přidat", command=self.add_ucitel).pack()

        self.tree = ttk.Treeview(self, columns=("ID", "Jméno", "Kabinet"), show="headings")
        for col in ("ID", "Jméno", "Kabinet"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        tk.Button(self, text="Smazat", command=self.delete_ucitel).pack()

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ucitele")

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    def add_ucitel(self):
        jmeno = self.entry_jmeno.get()
        kabinet = self.entry_kabinet.get()

        if not jmeno or not kabinet:
            messagebox.showerror("Chyba", "Vyplň všechna pole")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ucitele (jmeno, kabinet) VALUES (?, ?)", (jmeno, kabinet))
        conn.commit()
        conn.close()

        self.entry_jmeno.delete(0, tk.END)
        self.entry_kabinet.delete(0, tk.END)
        self.refresh()

    def delete_ucitel(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        id = item["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ucitele WHERE id=?", (id,))
        conn.commit()
        conn.close()

        self.refresh()
