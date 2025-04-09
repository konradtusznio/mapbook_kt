users: list=[
    {'name': 'Julia', 'location': 'Ząbki',  'posts': 10},
    {'name': 'Julia', 'location': 'Sokółka',  'posts': 20},
    {'name': 'Klaudia', 'location': 'Warszawa',  'posts': 15},
    {'name': 'Marcin', 'location': 'Grudziądz',  'posts': 1000},
    {'name': 'Mateusz', 'location': 'Lublin',  'posts': 100},
]



def get_user_info(users_data: list)->None:
    for user in users_data:
        print(f'Twój znajomy {user['name']} z miejscowości {user['location']} opublikował: {user["posts"]} postów')


print(f'Witaj {users[0]['name']}')
get_user_info(users[1:])








