from rich import print
from rich.prompt import Prompt
import os

DATA_FOLDER = "data"


def is_username_available(username):
    with open("userdb.txt", "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(",")
            if username == stored_username:
                return False
    return True


def create_new_user():
    username = Prompt.ask("Enter a username:")

    while not is_username_available(username):
        print("[bold red]Username already exists. Please choose a different username.")
        username = Prompt.ask("Enter a username:")

    password = Prompt.ask("Enter a password:", password=True)

    with open("userdb.txt", "a") as file:
        file.write(f"{username},{password}\n")

    print("[bold green]New user created successfully!")

    medical_history = Prompt.ask("Enter past medical history:")

    history_file = os.path.join(DATA_FOLDER, f"{username}_history.txt")
    with open(history_file, "w") as file:
        file.write(medical_history)

    print("[bold green]Past medical history saved!")


def verify_existing_user():
    username = Prompt.ask("Enter your username:")
    password = Prompt.ask("Enter your password:", password=True)

    with open("userdb.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if username == stored_username and password == stored_password:
                print("[bold green]User verification successful!")
                return username  # Return the username if successful

    print("[bold red]Invalid username or password.")
    return None


def check_medical_history(username):
    history_file = os.path.join(DATA_FOLDER, f"{username}_history.txt")
    if os.path.isfile(history_file):
        with open(history_file, "r") as file:
            return file.read()
    return None


def user_login():
    user_choice = Prompt.ask("Are you a new user? (y/n):")

    if user_choice.lower() == "y":
        create_new_user()
    else:
        username = verify_existing_user()
        if username:
            medical_history = check_medical_history(username)
            if medical_history:
                return medical_history
            else:
                print("[bold blue]No past medical history found.")
                return None


if __name__ == "__main__":
    user_login()
