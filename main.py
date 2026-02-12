import tkinter as tk
from tkinter import ttk
from database import create_tables
from predmety import PredmetyFrame
from ucitele import UciteleFrame
from rozvrh import RozvrhFrame


create_tables()

root = tk.Tk()
root.title("Správa rozvrhu žáků")
root.geometry("900x600")
root.minsize(800, 500)


style = ttk.Style()
style.theme_use("default")


notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

frame_predmety = PredmetyFrame(notebook)
frame_ucitele = UciteleFrame(notebook)
frame_rozvrh = RozvrhFrame(notebook)

notebook.add(frame_predmety, text="Předměty")
notebook.add(frame_ucitele, text="Učitelé")
notebook.add(frame_rozvrh, text="Rozvrh")

root.mainloop()
