from getpass import getpass
from instagrapi import Client

def ask_for_instagram_credentials():
    user_name = input("Please provide the Account user name: ")
    password = getpass(prompt="... and the associated password: ")
    return user_name, password

def get_instagram_client(user: str, passwd: str):
    cli = Client()
    cli.login(username=user, password=passwd)
    print("Login Successful!")

    return cli

if __name__ == "__main__":
    user, passwd = ask_for_instagram_credentials()
    cli = get_instagram_client(user, passwd)
