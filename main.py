from tkinter import *

import tkintermapview

users: list = []

def add_user()->None:
    name=entry_imie.get()
    surname=entry_nazwisko.get()
    location=entry_miejscowosc.get()
    posts=entry_posts.get()

    user = {'name':name, 'surname':surname, 'location':location, 'posts':posts}
    users.append(user)
    print(users)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_posts.delete(0, END)

    entry_imie.focus()

    show_users()


def show_users()->None:
    listbox_lista_obiektow.delete(0, END)
    for idx,user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f'{idx+1}.{user["name"]}')

def remove_user()->None:
    i = listbox_lista_obiektow.index(ACTIVE)
    users.pop(i)
    show_users()

def edit_user()->None:
    i = listbox_lista_obiektow.index(ACTIVE)
    name=users[i]['name']
    surname=users[i]['surname']
    location=users[i]['location']
    posts=users[i]['posts']

    entry_imie.insert(0,name)
    entry_nazwisko.insert(0,surname)
    entry_miejscowosc.insert(0,location)
    entry_posts.insert(0,posts)

    button_dodaj_obiekt.config(text='Zapisz', command=lambda: update_users(i))

def update_users(i)->None:
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    location = entry_miejscowosc.get()
    posts = entry_posts.get()

    users[i]['name'] = name
    users[i]['surname'] = surname
    users[i]['location'] = location
    users[i]['posts'] = posts

    show_users()

    button_dodaj_obiekt.config(text='Dodaj', command=add_user)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_posts.delete(0, END)

    entry_imie.focus()




root = Tk()
root.geometry("1200x700")
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

button_usun_obiekt=Button(ramka_lista_obiektow, text="Usuń", command=remove_user)
button_usun_obiekt.grid(row=2, column=1)

button_edytuj_obiekt=Button(ramka_lista_obiektow, text="Edytuj", command=edit_user)
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

button_dodaj_obiekt=Button(ramka_formularz, text="Dodaj", command=add_user)
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

label_szczegoly_obiektu_miejscowosc_wartsc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_obiektu_miejscowosc_wartsc.grid(row=1, column=5)

label_szczegoly_obiektu_miejscowosc_wartosc=Label(ramka_szczegoly_obiektow, text="Posty")
label_szczegoly_obiektu_miejscowosc_wartosc.grid(row=1, column=5)

label_szczegoly_obiektu_posts_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_obiektu_posts_wartosc.grid(row=1, column=6)


map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=800, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)









root.mainloop()

