import requests
from fake_useragent import UserAgent
import time
import os
from colorama import Fore, Back, Style, init

init(autoreset=True)  # Initialize colorama

# Function to clear the console
def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

# Input tokens and credentials
def get_credentials():
    tok = input(Back.RED + 'ENTER YOUR token Bot: ')
    io = input(Back.YELLOW + 'ENTER YOUR ID: ')
    clear_console()
    email = input(Back.RED + 'ENTER YOUR Username or Email IG: ')
    psw = input(Back.GREEN + 'ENTER YOUR Password: ')
    return tok, io, email, psw

def login_instagram(email, password):
    url = 'https://www.instagram.com/api/v1/web/accounts/login/ajax/'
    ua = UserAgent()
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.8',
        'content-length': '303',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'mid=ZQZC9QAEAAG9NicS3jBHkYqHlp8C; ig_nrcb=1; ig_did=AC6A65E6-8577-4CDE-8F3F-4B24D5787A91; datr=D0MGZZ_cUrCctc7jPE92HUgb; csrftoken=NYaOlpVmXUwzESZVfuFOYqbJ0gHzcvks',
        'dpr': '1',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/',
        'user-agent': ua.random,
        'viewport-width': '808',
        'x-asbd-id': '129477',
        'x-csrftoken': 'NYaOlpVmXUwzESZVfuFOYqbJ0gHzcvks',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-instagram-ajax': '1008686036',
        'x-requested-with': 'XMLHttpRequest',
    }

    # Generate timestamp for the password
    timestamp = str(int(time.time()))

    # Data payload for the login request
    data = {
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
        'optIntoOneTap': 'false',
        'queryParams': '{}',
        'trustedDeviceRecords': '{}',
        'username': email,
    }

    try:
        # Send the POST request to Instagram
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Check if the login was successful
        if "userId" in response.text:
            session_id = response.cookies.get("sessionid")
            return session_id
        else:
            print("Login failed. Response from Instagram:", response.text)
            return None
    except requests.RequestException as e:
        print(Fore.RED + "An error occurred: ", str(e))
        return None

def send_session_to_telegram(token, chat_id, session_id):
    if session_id:
        message = f'Your Session ID >> {session_id}\nBY >> @Zxyp9x'
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")
        print(message)
        with open("session.txt", "a") as file:
            file.write(f"Your Session >> {session_id}\n")
    else:
        print(Fore.RED + "Failed to retrieve session ID.")

def main():
    clear_console()
    tok, io, email, psw = get_credentials()
    session_id = login_instagram(email, psw)
    send_session_to_telegram(tok, io, session_id)

if __name__ == "__main__":
    main()
