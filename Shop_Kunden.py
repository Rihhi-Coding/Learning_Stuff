from datetime import date
import json
import openpyxl
"""German / Deutsch: 
Ein kleines Programm, welches durch eine Excel Tabelle geht, mit einstellbaren Zeilen z.B. 1-500 und alle Kunden, 
die offen sind zur Vertragsverlängerung (< 6 Monate Restlaufzeit) in einer JSON Datei ausgibt.
Die Vorraussetzung dafür ist eine Excel Tabelle ohne Störfaktoren, die pro Zeile, bei allen Kunden alle 
Werte vorhanden hat. Zum testen: Inhalt von Kundenliste.json löschen

English: 
This program iterates through an excel table (between selected rows, e.g. row 1 up to row 500) and
adds all customer to a JSON file, that could make a new contract (less than 6 months time left). It's important to
have a clean excel tabel, where all information are gathered. Empty fields would probably crash the switcher() func.
If you want to test, delete everything inside Kundenliste.json"""

excel_file = openpyxl.load_workbook('Test_Kundenliste.xlsx')        # Open Excel File
excel_sheet = excel_file['Tabelle1']                                # Select Table
cell_values = {}                                                    # Holds a temporary Dict from the table
category = {}                                                       # Holds the Key for the new Dict
switchcount = 1                                                     # To switch through the keys
printable = {}                                                      # the actual dict with the data of one row
vvl_able = False
tarife = ["Free", "Blau", "Grow", "VVL", "VV B"]
vvl_print = {}                                                 # +1 row, otherwise you won't get the last one
ident = 0
should_print = False


def laufzeit_calc(datum):
    global printable
    global vvl_able
    global tarife
    global vvl_print
    global should_print
    global ident
    umlaute = ["ä", "ö", "ü"]
    day = datum.day
    month = datum.month
    year = datum.year
    end_datum = date(year + 2, month, day)
    if int(month) >= 7:
        month = month - 6
    elif int(month) <= 6:
        month = 12 - 6 + month
        year = year - 1
    vvl_datum = date(year + 2, month, day)
    rest_lz = (end_datum.year - date.today().year) * 12 + end_datum.month - date.today().month
    print("______________________________")
    if vvl_datum < date.today():                            # checking if the customer can make a new contract
        vvl_able = True
        printable["VVL Datum"] = str(vvl_datum)
        printable["Restlaufzeit"] = str(rest_lz) + " Monate"
    else:
        vvl_able = False
        if "VVL Datum" in printable:
            del printable["VVL Datum"]
            del printable["Restlaufzeit"]
    for i in tarife:
        for u in umlaute:
            if u in printable["Nachname"]:                  # ä,ö,ü replacing in json file
                printable["Nachname"] = printable["Nachname"].replace("ö", "oe")
                printable["Nachname"] = printable["Nachname"].replace("ä", "ae")
                printable["Nachname"] = printable["Nachname"].replace("ü", "ue")
        if i in printable["Tarif"]:                         # only saving the important data
            ident = ident + 1
            should_print = True
            vvl_print["ID"] = ident
            vvl_print["Nachname"] = str(printable["Nachname"])
            vvl_print["Rufnummer"] = str(printable["Rufnummer"])
            vvl_print["PKK"] = str(printable["PKK"])
            vvl_print["Restlaufzeit"] = str(printable["Restlaufzeit"])
            vvl_print["VVL Datum"] = str(printable["VVL Datum"])
            vvl_print["Marke"] = i
# Calculates when the contract ends, how many months are left until end of contract, and when it's possible to make
# a new contract


def switcher():
    global category
    global switchcount
    global cell_values
    global excel_sheet
    global printable
    global vvl_able
    global vvl_print
    global should_print
    if switchcount == 1:
        category = "Mitarbeiter"
        switchcount += 1
    elif switchcount == 2:
        category = "Datum"
        switchcount += 1
    elif switchcount == 3:
        category = "Anrede"
        switchcount += 1
    elif switchcount == 4:
        category = "Geehrter"
        switchcount += 1
    elif switchcount == 5:
        category = "Nachname"
        switchcount += 1
    elif switchcount == 6:
        category = "Vorname"
        switchcount += 1
    elif switchcount == 7:
        category = "Strasse"
        switchcount += 1
    elif switchcount == 8:
        category = "Hausnummer"
        switchcount += 1
    elif switchcount == 9:
        category = "PLZ"
        switchcount += 1
    elif switchcount == 10:
        category = "Stadt"
        switchcount += 1
    elif switchcount == 11:
        category = "Geburtsdatum"
        switchcount += 1
    elif switchcount == 12:
        category = "Rufnummer"
        switchcount += 1
    elif switchcount == 13:
        category = "PKK"
        switchcount += 1
    elif switchcount == 14:
        category = "Tarif"
        switchcount += 1
    elif switchcount == 15:
        category = "Marke"
        switchcount += 1
    elif switchcount == 16:
        category = "Typ"
        switchcount += 1
    elif switchcount == 17:
        category = "Zuzahlung"
        switchcount += 1
    elif switchcount == 18:
        switchcount = 1
        printable = cell_values
        laufzeit_calc(printable["Datum"])
        printable["Datum"] = str(printable["Datum"])
        print(printable)
        if vvl_able and should_print:
            json.dump(vvl_print, open('Kundenliste.json', 'a'), indent=4, sort_keys=False)
            should_print = False
        switcher()
    else:
        print("Fail")
# Switches through switchcount, to add the correct key for every cell. Also after one customer is finished,
# it's added to an JSON file IF it's possible to make a new contract with the customer


for row_of_cells in excel_sheet['1':'126']:     # Always 1 row more than there is. If last row = 120 then 1:121
    for cell in row_of_cells:
        if cell.value is None:
            pass
        else:
            print(cell.value)
            switcher()
            cell_values[category] = cell.value
# iterates through all cells and saves the value in a dict, to use in switcher()
