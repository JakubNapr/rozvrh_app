import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection


class UciteleFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        #FORMULÁŘ 
        form_frame = ttk.LabelFrame(self, text="Přidat učitele", padding=10)
        form_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(form_frame, text="Jméno:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_jmeno = ttk.Entry(form_frame)
        self.entry_jmeno.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(form_frame, text="Kabinet:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_kabinet = ttk.Entry(form_frame)
        self.entry_kabinet.grid(row=1, column=1, sticky="ew", pady=2)

        form_frame.columnconfigure(1, weight=1)

        ttk.Button(form_frame, text="Přidat", command=self.add_ucitel)\
            .grid(row=2, column=0, columnspan=2, pady=5)

        #TREEVIEW
        table_frame = ttk.LabelFrame(self, text="Seznam učitelů", padding=5)
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Jméno", "Kabinet"),
            show="headings"
        )

        for col in ("ID", "Jméno", "Kabinet"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Jméno", anchor="w")
        self.tree.column("Kabinet", width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        #SMAZAT 
        ttk.Button(self, text="Smazat vybraného učitele", command=self.delete_ucitel)\
            .pack(pady=5)

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
        cursor.execute(
            "INSERT INTO ucitele (jmeno, kabinet) VALUES (?, ?)",
            (jmeno, kabinet)
        )
        conn.commit()
        conn.close()

        self.entry_jmeno.delete(0, tk.END)
        self.entry_kabinet.delete(0, tk.END)
        self.refresh()

    def delete_ucitel(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber učitele ke smazání")
            return

        item = self.tree.item(selected[0])
        ucitel_id = item["values"][0]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ucitele WHERE id=?", (ucitel_id,))
        conn.commit()
        conn.close()

        self.refresh()
