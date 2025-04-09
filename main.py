from utils.model import  users
from utils.controller import get_user_info

def main():
    print(f'Witaj {users[0]['name']}')
    get_user_info(users[1:])

if __name__ == '__main__':
    main()








