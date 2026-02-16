# rozvrh_app
Skupinový projekt do předmětu APR
---
## Popis projektu

Rozvrh App je konzolová aplikace napsaná v jazyce Python.
Slouží ke správě školního rozvrhu – umožňuje evidenci učitelů,
předmětů a vytváření rozvrhu hodin

Aplikace pracuje s databází SQLite, do které ukládá všechny údaje
Projekt je rozdělen do více modulů pro lepší přehlednost a organizaci kódu

---

## Cíl projektu

Cílem projektu bylo:

- Procvičit práci s databází SQLite
- Používat SQL příkazy (CREATE, INSERT, SELECT)
- Rozdělit projekt do více souborů (modulů)
- Vytvořit funkční databázovou aplikaci v Pythonu

---

## Použité technologie

- Python
- SQLite
- Modul sqlite3 (součást Pythonu)

SQLite jsme zvolili proto, že:
- Nepotřebuje server
- Je jednoduchá na použití
- Databáze je uložena v jednom souboru (.db)

---

## Struktura projektu

```
main.py        - hlavní spouštěcí soubor s menu
database.py    - připojení k databázi
ucitele.py     - správa učitelů
predmety.py    - správa předmětů
rozvrh.py      - práce s rozvrhem
rozvrh.db      - databázový soubor
README.md      - zde - dokumentace projektu
```

---

## Databáze

Projekt používá SQLite databázi `rozvrh.db`

Databáze obsahuje tabulky - 

- **ucitele** – seznam učitelů
- **predmety** – seznam předmětů
- **rozvrh** – propojení učitele, předmětu, dne a hodiny

Tabulka `rozvrh` obsahuje cizí klíče (FOREIGN KEY),
které propojují tabulky mezi sebou

---

## Spuštění projektu

1. Ujistíme se, že máte nainstalovaný Python 3
2. Otevřeme složku projektu
3. Spustíme příkaz:

```
python main.py
```

Po spuštění se zobrazí menu, ve kterém si uživatel vybírá jednotlivé možnosti

---

## Funkce aplikace

Aplikace umožňuje:

- Přidání učitele
- Přidání předmětu
- Vytvoření záznamu v rozvrhu
- Výpis uložených dat z databáze
