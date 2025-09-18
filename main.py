from tkinter import *
from tkinter import ttk
import tkintermapview
import re
from tkinter import messagebox

firmy: list = []
pracownicy: list = []
klienci: list = []


def dms_na_decimal(dms_str: str) -> float:
    match = re.match(r"(\d+)°(\d+)′(\d+)″([NSEW])", dms_str)

    stopnie = int(match.group(1))
    minuty = int(match.group(2))
    sekundy = int(match.group(3))
    kierunek = match.group(4)

    decimal = stopnie + minuty / 60 + sekundy / 3600
    if kierunek in ['S', 'W']:
        decimal = -decimal
    return decimal


def pobierz_wspolrzedne(miejscowosc: str) -> list[float | None]:
    from bs4 import BeautifulSoup
    import requests

    url = f"https://pl.wikipedia.org/wiki/{miejscowosc.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Błąd pobierania współrzędnych")
        return [None, None]

    soup = BeautifulSoup(response.content, "html.parser")
    lat_str = soup.select_one(".latitude")
    lon_str = soup.select_one(".longitude")

    if not lat_str or not lon_str:
        print("Błąd pobierania współrzędnych")
        return [None, None]

    lat = dms_na_decimal(lat_str.text)
    lon = dms_na_decimal(lon_str.text)
    return [lat, lon]

def _safe_marker(lat, lon, text):
    if lat is None or lon is None:
        messagebox.showwarning("Błąd", "Błędna miejscowość")
        return None
    return map_widget.set_marker(lat, lon, text=text)


class Firma:
    def __init__(self, nazwa, miejscowosc, map_widget):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.lat, self.lon = pobierz_wspolrzedne(miejscowosc)
        self.marker = _safe_marker(self.lat, self.lon, text=f'📦 {self.nazwa}')

class Pracownik:
    def __init__(self, imie, nazwisko, miejscowosc, nazwa_firmy, map_widget):
        self.imie = imie
        self.nazwisko = nazwisko
        self.miejscowosc = miejscowosc
        self.nazwa_firmy = nazwa_firmy
        self.lat, self.lon = pobierz_wspolrzedne(miejscowosc)
        self.marker = _safe_marker(self.lat, self.lon, text=f'🚚 {self.imie} {self.nazwisko}')

class Klient:
    def __init__(self, imie, nazwisko, miejscowosc, kurier: Pracownik, map_widget):
        self.imie = imie
        self.nazwisko = nazwisko
        self.miejscowosc = miejscowosc
        self.kurier = kurier
        self.lat, self.lon = pobierz_wspolrzedne(miejscowosc)
        self.marker = _safe_marker(self.lat, self.lon, text=f'🎯 {self.imie} {self.nazwisko}')


root = Tk()
root.geometry("1920x1080")
root.title("System zarządzania firmami kurierskimi")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

tab_firmy = Frame(notebook); notebook.add(tab_firmy, text="Firmy kurierskie")
ramka_lista_firm = Frame(tab_firmy); ramka_form_firm = Frame(tab_firmy)
ramka_lista_firm.grid(row=0, column=0, padx=10, pady=10)
ramka_form_firm.grid(row=0, column=1, padx=10, pady=10, sticky="n")

label_lista_firm = Label(ramka_lista_firm, text="Lista firm:")
label_lista_firm.pack()
listbox_firmy = Listbox(ramka_lista_firm, width=40, height=15)
listbox_firmy.pack()

label_form_firm = Label(ramka_form_firm, text="Nowa / edycja firmy")
label_form_firm.grid(row=0, column=0, columnspan=2)
Label(ramka_form_firm, text="Nazwa").grid(row=1, column=0, sticky=W)
Label(ramka_form_firm, text="Miejscowość").grid(row=2, column=0, sticky=W)
entry_firma_nazwa = Entry(ramka_form_firm); entry_firma_nazwa.grid(row=1, column=1)
entry_firma_miejsc = Entry(ramka_form_firm); entry_firma_miejsc.grid(row=2, column=1)

tab_prac = Frame(notebook); notebook.add(tab_prac, text="Pracownicy")
ramka_lista_prac = Frame(tab_prac); ramka_form_prac = Frame(tab_prac)
ramka_lista_prac.grid(row=0, column=0, padx=10, pady=10)
ramka_form_prac.grid(row=0, column=1, padx=10, pady=10, sticky="n")

label_lista_prac = Label(ramka_lista_prac, text="Lista pracowników:")
label_lista_prac.pack()
listbox_prac = Listbox(ramka_lista_prac, width=40, height=15)
listbox_prac.pack()

label_form_prac = Label(ramka_form_prac, text="Nowy / edycja pracownika")
label_form_prac.grid(row=0, column=0, columnspan=2)
Label(ramka_form_prac, text="Imię").grid(row=1, column=0, sticky=W)
Label(ramka_form_prac, text="Nazwisko").grid(row=2, column=0, sticky=W)
Label(ramka_form_prac, text="Miejscowość").grid(row=3, column=0, sticky=W)
Label(ramka_form_prac, text="Firma").grid(row=4, column=0, sticky=W)
entry_prac_imie = Entry(ramka_form_prac); entry_prac_imie.grid(row=1, column=1)
entry_prac_nazw = Entry(ramka_form_prac); entry_prac_nazw.grid(row=2, column=1)
entry_prac_miejsc = Entry(ramka_form_prac); entry_prac_miejsc.grid(row=3, column=1)
combo_prac_firma = ttk.Combobox(ramka_form_prac, state="readonly"); combo_prac_firma.grid(row=4, column=1)

tab_klienci = Frame(notebook); notebook.add(tab_klienci, text="Klienci")
ramka_lista_klien = Frame(tab_klienci); ramka_form_klien = Frame(tab_klienci)
ramka_lista_klien.grid(row=0, column=0, padx=10, pady=10)
ramka_form_klien.grid(row=0, column=1, padx=10, pady=10, sticky="n")

label_lista_klien = Label(ramka_lista_klien, text="Lista klientów:")
label_lista_klien.pack()
listbox_klien = Listbox(ramka_lista_klien, width=40, height=15)
listbox_klien.pack()

label_form_klien = Label(ramka_form_klien, text="Nowy / edycja klienta")
label_form_klien.grid(row=0, column=0, columnspan=2)
Label(ramka_form_klien, text="Imię").grid(row=1, column=0, sticky=W)
Label(ramka_form_klien, text="Nazwisko").grid(row=2, column=0, sticky=W)
Label(ramka_form_klien, text="Miejscowość").grid(row=3, column=0, sticky=W)
Label(ramka_form_klien, text="Kurier").grid(row=4, column=0, sticky=W)
entry_klien_imie = Entry(ramka_form_klien); entry_klien_imie.grid(row=1, column=1)
entry_klien_nazw = Entry(ramka_form_klien); entry_klien_nazw.grid(row=2, column=1)
entry_klien_miejsc = Entry(ramka_form_klien); entry_klien_miejsc.grid(row=3, column=1)
combo_klien_kurier = ttk.Combobox(ramka_form_klien, state="readonly"); combo_klien_kurier.grid(row=4, column=1)

tab_mapa = Frame(notebook); notebook.add(tab_mapa, text="Mapa")
map_widget = tkintermapview.TkinterMapView(tab_mapa, width=800, height=650, corner_radius=0)
map_widget.pack(side=LEFT, padx=10, pady=10)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

ramka_przyciski_mapy = Frame(tab_mapa)
ramka_przyciski_mapy.pack(side=RIGHT, padx=10, pady=10, fill=Y)

btn_all_firmy = Button(ramka_przyciski_mapy, text="Mapa wszystkich firm")
btn_all_prac = Button(ramka_przyciski_mapy, text="Mapa wszystkich pracowników")
btn_klien_kur = Button(ramka_przyciski_mapy, text="Mapa klientów\nwybranego kuriera")
btn_prac_firmy = Button(ramka_przyciski_mapy, text="Mapa pracowników\nwybranej firmy")

btn_all_firmy.pack(fill=X, pady=2)
btn_all_prac.pack(fill=X, pady=2)
btn_klien_kur.pack(fill=X, pady=2)
btn_prac_firmy.pack(fill=X, pady=2)


ramka_panel_mapy = Frame(tab_mapa)
ramka_panel_mapy.pack(side=RIGHT, fill=Y, padx=10, pady=10)

notebook_mapy = ttk.Notebook(ramka_panel_mapy)
notebook_mapy.pack(fill=BOTH, expand=True)


frame_map_firmy = Frame(notebook_mapy); notebook_mapy.add(frame_map_firmy, text="Firmy")
listbox_mapa_firmy = Listbox(frame_map_firmy, selectmode=MULTIPLE, width=35, height=15)
listbox_mapa_firmy.pack(padx=4, pady=(4,0))
btn_show_firmy = Button(frame_map_firmy, text="Pokaż zaznaczone firmy",
                        command=lambda: mapa_zaznaczone_firmy())
btn_show_firmy.pack(fill=X, padx=4, pady=4)


frame_map_prac = Frame(notebook_mapy); notebook_mapy.add(frame_map_prac, text="Pracownicy")
listbox_mapa_prac = Listbox(frame_map_prac, selectmode=MULTIPLE, width=35, height=15)
listbox_mapa_prac.pack(padx=4, pady=(4,0))
btn_show_prac = Button(frame_map_prac, text="Pokaż zaznaczonych pracowników",
                       command=lambda: mapa_zaznaczeni_prac())
btn_show_prac.pack(fill=X, padx=4, pady=4)


frame_map_klien = Frame(notebook_mapy); notebook_mapy.add(frame_map_klien, text="Klienci")
listbox_mapa_klien = Listbox(frame_map_klien, selectmode=MULTIPLE, width=35, height=15)
listbox_mapa_klien.pack(padx=4, pady=(4,0))
btn_show_klien = Button(frame_map_klien, text="Pokaż zaznaczonych klientów",
                        command=lambda: mapa_zaznaczeni_klienci())
btn_show_klien.pack(fill=X, padx=4, pady=4)


def odswiez_listy():


    listbox_firmy.delete(0, END)
    for i, f in enumerate(firmy):
        listbox_firmy.insert(i, f'{i+1}. {f.nazwa} ({f.miejscowosc})')

    combo_prac_firma['values'] = [f.nazwa for f in firmy]
    listbox_prac.delete(0, END)
    for i, p in enumerate(pracownicy):
        listbox_prac.insert(i, f'{i+1}. {p.imie} {p.nazwisko} – {p.nazwa_firmy}')


    combo_klien_kurier['values'] = [f'{p.imie} {p.nazwisko}' for p in pracownicy]
    listbox_klien.delete(0, END)
    for i, k in enumerate(klienci):
        listbox_klien.insert(i, f'{i+1}. {k.imie} {k.nazwisko} (kurier: {k.kurier.imie} {k.kurier.nazwisko})')

    listbox_mapa_firmy.delete(0, END)
    for i, f in enumerate(firmy):
        listbox_mapa_firmy.insert(i, f"{i+1}. {f.nazwa} ({f.miejscowosc})")

    listbox_mapa_prac.delete(0, END)
    for i, p in enumerate(pracownicy):
        listbox_mapa_prac.insert(i, f"{i+1}. {p.imie} {p.nazwisko} – {p.nazwa_firmy}")

    listbox_mapa_klien.delete(0, END)
    for i, k in enumerate(klienci):
        listbox_mapa_klien.insert(i, f"{i+1}. {k.imie} {k.nazwisko} (kurier: {k.kurier.imie} {k.kurier.nazwisko})")


def wyczysc_formularze():
    entry_firma_nazwa.delete(0, END); entry_firma_miejsc.delete(0, END)
    entry_prac_imie.delete(0, END); entry_prac_nazw.delete(0, END); entry_prac_miejsc.delete(0, END)
    entry_klien_imie.delete(0, END); entry_klien_nazw.delete(0, END); entry_klien_miejsc.delete(0, END)
    combo_prac_firma.set(''); combo_klien_kurier.set('')

def wyczysc_markery():

    for ob in firmy + pracownicy + klienci:
        if ob.marker:
            ob.marker.delete()


def _pokaz_zaznaczone(listbox, obiekty, ikonka):

    indeksy = listbox.curselection()
    if not indeksy:
        messagebox.showwarning("Brak wyboru",
                               "Zaznacz co najmniej jedną pozycję na liście.")
        return

    wyczysc_markery()
    postawionych = 0
    first_lat, first_lon = None, None

    for idx in indeksy:
        obj = obiekty[idx]
        marker = _safe_marker(obj.lat, obj.lon,
                              text=f"{ikonka} {getattr(obj, 'nazwa', getattr(obj, 'imie', ''))} "
                                   f"{getattr(obj, 'nazwisko', '')}")
        obj.marker = marker
        if marker:
            postawionych += 1
            if first_lat is None:
                first_lat, first_lon = obj.lat, obj.lon

    if postawionych == 0:
        messagebox.showwarning("Brak współrzędnych",
                               "Żaden z wybranych obiektów nie ma poprawnych współrzędnych.")
        return


    if first_lat is not None:
        map_widget.set_position(first_lat, first_lon)
        map_widget.set_zoom(8)

def mapa_zaznaczone_firmy():
    _pokaz_zaznaczone(listbox_mapa_firmy, firmy, "🏢")

def mapa_zaznaczeni_prac():
    _pokaz_zaznaczone(listbox_mapa_prac, pracownicy, "🚚")

def mapa_zaznaczeni_klienci():
    _pokaz_zaznaczone(listbox_mapa_klien, klienci, "🎯")

def dodaj_firme() -> None:
    nazwa = entry_firma_nazwa.get()
    miejsc = entry_firma_miejsc.get()
    if not (nazwa and miejsc):
        return
    lat, lon = pobierz_wspolrzedne(miejsc)
    if lat is None or lon is None:
        messagebox.showwarning("Błąd", "Nie udało się pobrać współrzędnych dla tej miejscowości.")
        return
    firma = Firma(nazwa, miejsc, map_widget)
    firmy.append(firma)
    odswiez_listy(); wyczysc_formularze()

def usun_firme():
    sel = listbox_firmy.curselection()
    if not sel:
        return
    idx = sel[0]
    firma_nazwa = firmy[idx].nazwa
    firmy[idx].marker.delete()
    firmy.pop(idx)
    for p in pracownicy[:]:
        if p.nazwa_firmy == firma_nazwa:
            p.marker.delete()
            pracownicy.remove(p)

    odswiez_listy()

def dodaj_pracownika():
    imie = entry_prac_imie.get()
    nazw = entry_prac_nazw.get()
    miej = entry_prac_miejsc.get()
    firma = combo_prac_firma.get()
    if not (imie and nazw and miej and firma):
        return
    lat, lon = pobierz_wspolrzedne(miej)
    if lat is None or lon is None:
        return
    p = Pracownik(imie, nazw, miej, firma, map_widget)
    pracownicy.append(p)
    odswiez_listy(); wyczysc_formularze()

def usun_pracownika():
    sel = listbox_prac.curselection()
    if not sel:
        return
    idx = sel[0]
    pracownicy[idx].marker.delete()
    for k in klienci[:]:
        if k.kurier == pracownicy[idx]:
            k.marker.delete()
            klienci.remove(k)
    pracownicy.pop(idx)
    odswiez_listy()

def dodaj_klienta():
    imie = entry_klien_imie.get()
    nazw = entry_klien_nazw.get()
    miej = entry_klien_miejsc.get()
    kurier_str = combo_klien_kurier.get()
    if not (imie and nazw and miej and kurier_str):
        return
    kurier = next((p for p in pracownicy if f'{p.imie} {p.nazwisko}' == kurier_str), None)
    if not kurier:
        return
    lat, lon = pobierz_wspolrzedne(miej)
    if lat is None or lon is None:
        messagebox.showwarning("Błąd", "Nie udało się pobrać współrzędnych dla tej miejscowości.")
        return
    k = Klient(imie, nazw, miej, kurier, map_widget)
    klienci.append(k)
    odswiez_listy(); wyczysc_formularze()

def usun_klienta():
    sel = listbox_klien.curselection()
    if not sel:
        return
    idx = sel[0]
    klienci[idx].marker.delete()
    klienci.pop(idx)
    odswiez_listy()


Button(ramka_form_firm, text="Dodaj firmę", command=dodaj_firme, width=18).grid(row=3, column=0, columnspan=2, pady=4)
Button(ramka_lista_firm, text="Usuń zaznaczoną firmę", command=usun_firme).pack(pady=2)

Button(ramka_form_prac, text="Dodaj pracownika", command=dodaj_pracownika, width=18).grid(row=5, column=0, columnspan=2, pady=4)
Button(ramka_lista_prac, text="Usuń zaznaczonego", command=usun_pracownika).pack(pady=2)

Button(ramka_form_klien, text="Dodaj klienta", command=dodaj_klienta, width=18).grid(row=5, column=0, columnspan=2, pady=4)
Button(ramka_lista_klien, text="Usuń zaznaczonego", command=usun_klienta).pack(pady=2)


def mapa_wszystkich_firm():
    wyczysc_markery()
    for f in firmy:
        f.marker = map_widget.set_marker(f.lat, f.lon, text=f'📦 {f.nazwa}')
    map_widget.set_zoom(6)

def mapa_wszystkich_pracownikow():
    wyczysc_markery()
    for p in pracownicy:
        p.marker = map_widget.set_marker(p.lat, p.lon, text=f'🚚 {p.imie} {p.nazwisko}')
    map_widget.set_zoom(6)

def mapa_klientow_kuriera():

    sel = listbox_prac.curselection()
    if not sel:
        messagebox.showwarning(
            "Brak wyboru",
            "Najpierw zaznacz kuriera w zakładce »Pracownicy«."
        )
        return

    wyczysc_markery()

    kurier = pracownicy[sel[0]]
    klienci_kuriera = [k for k in klienci if k.kurier == kurier]

    if not klienci_kuriera:
        messagebox.showinfo(
            "Brak klientów",
            f"Kurier {kurier.imie} {kurier.nazwisko} nie ma jeszcze przypisanych klientów."
        )
        return

    postawionych = 0

    kurier.marker = _safe_marker(
        kurier.lat, kurier.lon, text=f'⭐ {kurier.imie} {kurier.nazwisko}'
    )
    if kurier.marker:
        postawionych += 1

    for k in klienci_kuriera:
        m = _safe_marker(k.lat, k.lon, text=f'🎯 {k.imie} {k.nazwisko}')
        k.marker = m
        if m:
            postawionych += 1

    if postawionych == 0:
        messagebox.showwarning(
            "Brak współrzędnych",
            "Ani kurier, ani żaden z jego klientów nie ma poprawnych współrzędnych "
            "(Błąd pobierania współrzędnych)."
        )
        return


    if kurier.lat is not None:
        map_widget.set_zoom(8)
        map_widget.set_position(kurier.lat, kurier.lon)


def mapa_pracownikow_firmy():

    sel = listbox_firmy.curselection()
    if not sel:
        messagebox.showwarning(
            "Brak wyboru",
            "Najpierw zaznacz firmę w zakładce »Firmy kurierskie«."
        )
        return

    wyczysc_markery()

    firma = firmy[sel[0]]
    prac_firmy = [p for p in pracownicy if p.nazwa_firmy == firma.nazwa]

    if not prac_firmy:
        messagebox.showinfo(
            "Brak pracowników",
            f"Firma {firma.nazwa} nie ma jeszcze dodanych pracowników."
        )
        return

    postawionych = 0

    firma.marker = _safe_marker(
        firma.lat, firma.lon, text=f'🏢 {firma.nazwa}'
    )
    if firma.marker:
        postawionych += 1

    for p in prac_firmy:
        m = _safe_marker(p.lat, p.lon, text=f'🚚 {p.imie} {p.nazwisko}')
        p.marker = m
        if m:
            postawionych += 1

    if postawionych == 0:
        messagebox.showwarning(
            "Brak współrzędnych",
            "Ani siedziba firmy, ani żaden z jej pracowników nie posiada poprawnych "
            "współrzędnych (Błąd pobierania współrzędnych)."
        )
        return

    if firma.lat is not None:
        map_widget.set_zoom(8)
        map_widget.set_position(firma.lat, firma.lon)


btn_all_firmy.config(command=mapa_wszystkich_firm)
btn_all_prac.config(command=mapa_wszystkich_pracownikow)
btn_klien_kur.config(command=mapa_klientow_kuriera)
btn_prac_firmy.config(command=mapa_pracownikow_firmy)



odswiez_listy()
root.mainloop()
