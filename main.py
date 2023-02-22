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
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode().decode())

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]

    def random_pass(self):
        while True:
            password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20))
            if (any(c.islower() for c in password) and any(c.isupper() for c in password) and 
                sum(c.isdigit() for c in password) >= 2 and sum(c in string.punctuation for c in password) >= 2):
                return password

def main():
    password = {
        "email" : "1234567",
        "Facebook" : "myfbpassword",
        "youtube" : "hello123",
        "something" : "testpassword_1234"
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
            print("Do you want a randomly generated password? (y/n)")
            random = input("Enter your choice: ")
            if random == "y":
                password = pm.random_pass()
                print("new password is: " + password)
            else:
                password = input("Enter the password: ")
            pm.add_password(site, password)
        elif choice == "6":
            continue
        elif choice == "7":
            site = input("What site do you want: ")
            print(f"Password for {site} is: {pm.get_password(site)}")
        elif choice == "8":
            menu()
        elif choice.lower() == "q" or "quit":
            done = True
            print("Bye")
        else:
            print("Invalid choice")

def menu ():
    print("""What do you want to do? \n
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Update a password
    (7) Get a password
    (8) See menu again
    (q) Quit
    """)

if __name__ == "__main__":
    main()