import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


class PredmetyFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        #FORMULÁŘ
        form_frame = ttk.LabelFrame(self, text="Přidat předmět", padding=10)
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Název:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_nazev = ttk.Entry(form_frame)
        self.entry_nazev.grid(row=0, column=1, pady=2, sticky="ew")

        ttk.Label(form_frame, text="Zkratka:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_zkratka = ttk.Entry(form_frame)
        self.entry_zkratka.grid(row=1, column=1, pady=2, sticky="ew")

        form_frame.columnconfigure(1, weight=1)

        ttk.Button(form_frame, text="Přidat", command=self.add_predmet)\
            .grid(row=2, column=0, columnspan=2, pady=5)

        #TREEVIEW
        table_frame = ttk.LabelFrame(self, text="Seznam předmětů", padding=5)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Název", "Zkratka"),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Název", text="Název")
        self.tree.heading("Zkratka", text="Zkratka")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Název", anchor="w")
        self.tree.column("Zkratka", width=100, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        #TLAČÍTKO SMAZAT
        ttk.Button(self, text="Smazat vybraný předmět", command=self.delete_predmet)\
            .pack(pady=5)

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
        cursor.execute(
            "INSERT INTO predmety (nazev, zkratka) VALUES (?, ?)",
            (nazev, zkratka)
        )
        conn.commit()
        conn.close()

        self.entry_nazev.delete(0, tk.END)
        self.entry_zkratka.delete(0, tk.END)
        self.refresh()

    def delete_predmet(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber předmět ke smazání")
            return

        item = self.tree.item(selected[0])
        predmet_id = item["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predmety WHERE id=?", (predmet_id,))
        conn.commit()
        conn.close()

        self.refresh()


