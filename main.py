from tkinter import *

import tkintermapview

root = Tk()

root.geometry("1000x600")
root.title('mapbook_kt')

ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# ramka_lista_obiektow

label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista użytkowników:")
label_lista_obiektow.grid(row=0, column=0)

listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

button_pokaz_szczegoly=Button(ramka_lista_obiektow, text="Pokaż szczegóły")
button_pokaz_szczegoly.grid(row=2, column=0)

button_usun_obiekt=Button(ramka_lista_obiektow, text="Usuń")
button_usun_obiekt.grid(row=2, column=1)

button_edytuj_obiekt=Button(ramka_lista_obiektow, text="Edytuj")
button_edytuj_obiekt.grid(row=2, column=2)

#ramka_formularz

label_formularz=Label(ramka_formularz, text="Formularz:")
label_formularz.grid(row=0, column=0)

label_imie=Label(ramka_formularz, text="Imie:")
label_imie.grid(row=1, column=0, sticky=W)

label_nazwisko=Label(ramka_formularz, text="Nazwisko:")
label_nazwisko.grid(row=2, column=0, sticky=W)

label_miejscowosc=Label(ramka_formularz, text="Miejscowość:")
label_miejscowosc.grid(row=3, column=0, sticky=W)

label_posts=Label(ramka_formularz, text="Posty:")
label_posts.grid(row=4, column=0, sticky=W)

entry_imie=Entry(ramka_formularz)
entry_imie.grid(row=1, column=1)

entry_nazwisko=Entry(ramka_formularz)
entry_nazwisko.grid(row=2, column=1)

entry_miejscowosc=Entry(ramka_formularz)
entry_miejscowosc.grid(row=3, column=1)

entry_posts=Entry(ramka_formularz)
entry_posts.grid(row=4, column=1)

button_dodaj_obiekt=Button(ramka_formularz, text="Dodaj")
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

# ramka_szczegoly_obiektow

label_pokaz_szczegoly=Label(ramka_szczegoly_obiektow, text="Szczegóły użytkownika:")
label_pokaz_szczegoly.grid(row=0, column=0)

label_szczegoly_obiektu_name=Label(ramka_szczegoly_obiektow, text="Imię:")
label_szczegoly_obiektu_name.grid(row=1, column=0)

label_szczegoly_obiektu_name_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_obiektu_name_wartosc.grid(row=1, column=1)

label_szczegoly_obiektu_surname=Label(ramka_szczegoly_obiektow, text="Nazwisko")
label_szczegoly_obiektu_surname.grid(row=1, column=2)

label_szczegoly_obiektu_surname_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_obiektu_surname_wartosc.grid(row=1, column=3)

label_szczegoly_obiektu_miejscowosc=Label(ramka_szczegoly_obiektow, text="Miejscowosc")
label_szczegoly_obiektu_miejscowosc.grid(row=1, column=4)

label_szczegoly_obiektu_miejscowosc_wartosc=Label(ramka_szczegoly_obiektow, text="Posty")
label_szczegoly_obiektu_miejscowosc_wartosc.grid(row=1, column=4)

label_szczegoly_obiektu_posts_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_obiektu_posts_wartosc.grid(row=1, column=5)


map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=800, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)









root.mainloop()

