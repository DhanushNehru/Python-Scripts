from cryptography.fernet import Fernet
# Symmetric Key Encyrption Class

# Password Manager Class that will create & load passwords from an encrypted file
class PasswordManager:
    def __init__(self):
        self.key = None
        self.pwd_file = None
        self.pwd_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    # init_values is a dictionary
    def create_pwd_file(self, path, init_values=None):
        self.pwd_file = path
        if init_values is not None:
            for key, values in init_values.items():
                self.add_password(self, key, values)

    def load_pwd_file(self, path):
        self.pwd_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                # Loads the site and the associated encrypted password. Password must be encoded before decyprtion and decoded before returning text
                self.pwd_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.pwd_dict[site] = password
        if self.pwd_file is not None:
            with open(self.pwd_file, 'a') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                s = ":"
                written = site + s + encrypted.decode() + "\n"
                f.write(written)

    def get_password(self, site):
        return self.pwd_dict[site]
    
    def get_sites(self):
        print("List of Sites:")
        for a in self.pwd_dict.keys():
            print(a)

def main():
    pm = PasswordManager()
    print("""What would you like to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password for a site
    (7) Get the list of sites
    (m) Menu
    (h) Help
    (q) Quit""")
    done = False

    while not done:

        choice = input("Enter your choice: ")
        choice = choice.lower()
        match choice:
            case "1":
                path = input("Enter the path: ")
                pm.create_key(path)
            case "2":
                path = input("Enter the path: ")
                pm.load_key(path)
            case "3":
                path = input("Enter the path: ")
                pm.create_pwd_file(path, init_values=None)
            case "4":
                path = input ("Enter the path: ")
                pm.load_pwd_file(path)
            case "5":
                site = input("Enter the site: ")
                password = input("Enter the password: ")
                pm.add_password(site, password)
            case "6":
                site = input("What site do you want: ")
                print(pm.get_password(site))
            case "7":
                pm.get_sites()
            case "m":
                print("""What would you like to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load existing password file
    (5) Add a new password
    (6) Get a password for a site
    (m) Menu
    (h) Help
    (q) Quit""")
            case "h": 
                print("""Getting Started:
    1.  Select Option (1) Create a new key that will be used to encrypt your password file.
    2.  Select Option (3) Create a new password file that will be used to hold your encrypted passwords.
    3.  Select Option (5) Add a new password to the password file. \n
Retrieving or Adding Passords:
    1.  Select Option (2) Load the existing key so it can be used to encrypt new passwords or retrieve passwords from the password file.
    2.  Select Option (4) Load the existing password file so it can be used to add or retrieve passwords.
    3a. Select Option (5) Add a new password to the password file.
    3b. Select Option (6) Retrieve a password for a site.""")
            case "q":
                done = True
                print("Bye!")
            case _:
                print("Invalid Choice!")

if __name__ == '__main__':
    main()