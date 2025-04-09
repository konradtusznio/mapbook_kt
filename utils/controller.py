def get_user_info(users_data: list)->None:
    for user in users_data:
        print(f'Twój znajomy {user['name']} z miejscowości {user['location']} opublikował: {user["posts"]} postów')

def add_user(users_data: list)-> None:
    new_name:str = input('Podaj imię nowego znajomego: ')
    new_location:str = input('Podaj lokalizację: ')
    new_post:int = int(input('Podaj liczbę postów: '))
    users_data.append({'name': new_name, 'location': new_location,  'posts': new_post})


