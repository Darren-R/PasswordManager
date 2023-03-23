from cryptography.fernet import Fernet
import string
import random


class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        try:
            with open(path, 'rb') as f:
                self.key = f.read()
        except FileNotFoundError:
            print(f"File {path} not located.")

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for site, values in initial_values.items():
                for key, value in values.items():
                    self.add_password(site, key, value)

    def load_password_file(self, path):
        self.password_file = path

        try:
            with open(path, 'r') as f:
                for line in f:
                    site, encrypted = line.strip().split(":")
                    username_encrypted, password_encrypted = encrypted.split(
                        "+")
                    if site not in self.password_dict:
                        self.password_dict[site] = {}
                    username = Fernet(self.key).decrypt(
                        username_encrypted.encode()).decode()
                    password = Fernet(self.key).decrypt(
                        password_encrypted.encode()).decode()
                    self.password_dict[site][username] = password
        except FileNotFoundError:
            print(f"File {path} not located.")

    def add_password(self, site, username, password):
        if site not in self.password_dict:
            self.password_dict[site] = {}
        encrypted_username = Fernet(self.key).encrypt(
            username.encode()).decode()
        encrypted_password = Fernet(self.key).encrypt(
            password.encode()).decode()
        encrypted = encrypted_username + "+" + encrypted_password
        self.password_dict[site][encrypted_username] = password

        if self.password_file is not None:
            with open(self.password_file, 'a') as f:
                f.write(site + ":" + encrypted + "\n")

    def get_password(self, site):
        try:
            user, password = list(self.password_dict[site].items())[0]
            return print(f"Username: {user}\nPassword: {password}")
        except KeyError:
            return None, None

    def show_all_apps(self):
        print("")
        if len(self.password_dict) > 0:
            for site, passwords in self.password_dict.items():
                print(f"Passwords held for application: {site}")
        else:
            print("No passwords saved.")

    def random_pass(self):
        while True:
            password = ''.join(random.choice(
                string.ascii_letters + string.digits + string.punctuation) for i in range(20))
            if (any(c.islower() for c in password) and any(c.isupper() for c in password) and
                    sum(c.isdigit() for c in password) >= 2 and sum(c in string.punctuation for c in password) >= 2):
                return password

    def delete_password(self, site, username=None):
        if site in self.password_dict:
            if username is None:
                del self.password_dict[site]
                print(f"Deleted all passwords for site: {site}")
            else:
                encrypted_username = Fernet(self.key).encrypt(
                    username.encode()).decode()
                if encrypted_username in self.password_dict[site]:
                    del self.password_dict[site][encrypted_username]
                    print(
                        f"Deleted password for user {username} on site {site}")
                else:
                    print(
                        f"No password found for user {username} on site {site}")
        else:
            print(f"No passwords found for site {site}")

        self._update_password_file()

    def _update_password_file(self):
        if self.password_file is not None:
            with open(self.password_file, 'w') as f:
                for site, passwords in self.password_dict.items():
                    for encrypted_username, password in passwords.items():
                        encrypted_password = Fernet(self.key).encrypt(
                            password.encode()).decode()
                        encrypted = encrypted_username + "+" + encrypted_password
                        f.write(site + ":" + encrypted + "\n")


def main():
    password = {
        "email": {"Darren@gmail.com": "12345"},
        "Facebook": {"Darren R": "myfbpassword"},
    }

    pm = PasswordManager()

    menu()

    done = False

    while not done:

        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif choice == "5":
            site = input("Enter the site: ")
            key = input("Enter your username: ")
            print("Do you want a randomly generated password? (y/n)")
            random = input("Enter your choice: ")
            if random == "y":
                password = pm.random_pass()
            else:
                password = input("Enter the password: ")
            print("Username: " + key)
            print("Password: " + password)
            pm.add_password(site, key, password)
        elif choice == "6":
            pm.show_all_apps()
        elif choice == "7":
            site = input("What site do you want: ")
            pm.get_password(site)
        elif choice == "8":
            site = input("Enter the site: ")
            pm.delete_password(site)
        elif choice == "9":
            menu()
        elif choice.lower() == "q" or "quit":
            done = True
            print("Bye")
        else:
            print("Invalid choice")


def menu():
    print("""\nWhat do you want to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Applications saved
    (7) Get a password
    (8) Delete a password
    (9) See Menu again
    (q) Quit
    """)


if __name__ == "__main__":
    main()
