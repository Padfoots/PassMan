import base64
import binascii
from getpass import getpass
from rich import print as printr
from tabulate import tabulate
from account import NewAccount, Account
import aes
from utils import db
import re
import argon
import random
import string
import pyperclip

class User:
    def __init__(self,id, email, master_key, master_password, vault_id=None, vault_key_salt=None):
        self.id = id
        self.email = email
        self.master_password = master_password
        self.master_key = master_key
        self.vault_id = vault_id
        self.vault_key_salt = vault_key_salt
        self.accounts = self.get_accounts()
    def get_vault_key(self):
        vault_key = argon.compute_vault_key(self.email,self.master_password,self.vault_key_salt)
        vault_key_decoded = base64.urlsafe_b64decode(vault_key + '==')
        return vault_key_decoded


    def add_account(self):
        name = input("name: ")
        user_name = input("username: ")
        email = input("email: ")
        url = input("url: ")

        # TODO: YOU NEED TO CREATE A VALIDATION FOR THE INPUT
        type = input("type [password,bank account, secure note, payment card]: ")


        while True:
            password = getpass("password[press enter to generate a password]: ")
            if not password:
                password_length = input("choose password length: ")
                password = generate_password(int(password_length))
                break

                # call the generator function
            # TODO: set a default option for password if it is null call the password
            # generator function
            score = rate_password_strength(password)
            rating = password_strength_rating(score)
            if score >= 6:
                printr(f"[green][+] Password Rating: {rating} [/green]")
            else:
                printr(f"[red][-] Password Rating: {rating}  [/red]")
                printr("[yellow][!] Are you sure you want to save that Password[Y/n] [/yellow]")
                choice = input()
                while choice.lower() != 'y' and choice.lower() != 'n':
                    printr("[red][-] Y/n: [/red]")
                    choice = input()
                if choice.lower() == 'n':
                    continue
            password_confirmation = getpass("Confirm password: ")
            while password != password_confirmation:
                printr("[red][-] Password Do Not Match [/red]")
                password_confirmation = getpass("Confirm password: ")
            printr("[green][+] Password Confirmed [/green]")

            aes_key = self.get_vault_key()
            encryptedMsg = aes.encrypt_AES_GCM(password.encode('utf-8'), aes_key)
            encrypted_password = binascii.hexlify(encryptedMsg[0])
            aes_iv = binascii.hexlify(encryptedMsg[1])
            auth_tag = binascii.hexlify(encryptedMsg[2])

            new_account = NewAccount(self.vault_id, name, email, encrypted_password,
                                     url, aes_iv, auth_tag, user_name, type)

            db.new_account(new_account)
            self.accounts = self.get_accounts()
            printr("[green][+] Account added to your Vault successfully [/green]")
            return


    def get_accounts(self):
        rows = db.get_vault_accounts(self.vault_id)
        if rows:
            accounts = [Account(**row) for row in rows if row]
            return accounts
        return []

    # create a function that takes an account object and decrypts an account password
    # call the copy to clipboard function with the decrypted password
    def get_account_password(self,account_id):
        #TODO: WE TAKE THE ACCOUNT ID
        # WE ITERATE OVER THE USER OBJECT'S LIST OF ACCOUNTS TILL FIND THE ID
        account = next((acc for acc in self.accounts if acc.id == account_id), None)
        if not account:
            print("Account not found.")
            return None
        vault_key = self.get_vault_key()
        account_password = aes.decrypt_AES_GCM(account.password,
                                               account.aes_iv,account.auth_tag,
                                               vault_key)
        copy_to_clipboard(account_password)

    def get_account(self, account_name):
        accounts = [acc for acc in self.accounts if acc.name == account_name]
        if not accounts:
            return None
        return accounts



def rate_password_strength(password):
    score = 0

    # Length check
    length = len(password)
    if length >= 12:
        score += 3
    elif length >= 8:
        score += 2

    # Complexity checks
    if re.search(r'[A-Z]', password):  # Uppercase letter
        score += 1
    if re.search(r'[a-z]', password):  # Lowercase letter
        score += 1
    if re.search(r'[0-9]', password):  # Digit
        score += 1
    if re.search(r'[@#$%^&*!]', password):  # Special character
        score += 1

    # Check for common patterns
    common_patterns = [
        r'password', r'123456', r'12345678', r'12345',
        r'qwerty', r'abc123', r'password1', r'admin',
    ]
    for pattern in common_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            score -= 2
            break  # Only need to check once

    # Check for repeated sequences
    if re.search(r'(.)\1{2,}', password):
        score -= 2

    # Ensure the score is between 0 and 10
    score = max(0, min(score, 10))

    return score


def password_strength_rating(score):

    if score == 10:
        return "Excellent"
    elif score >= 8:
        return "Very Strong"
    elif score >= 6:
        return "Strong"
    elif score >= 4:
        return "Moderate"
    elif score >= 2:
        return "Weak"
    else:
        return "Very Weak"


def register():
    while True:
        email = input("email: ")
        master_password = validate_password()
        master_key_hash, vault_key_salt, vault_key_hash = argon.generate_master_key(email, master_password)
        new_user_id = db.new_user(email,master_key_hash)
        db.new_vault(new_user_id,vault_key_salt)
        printr("[green][+] User Created successfully [/green]")
        break


def validate_password():
    score = 0
    wrong_validation = True
    while score < 6 or wrong_validation:
        master_password = getpass("Master Password: ")
        score = rate_password_strength(master_password)
        rating = password_strength_rating(score)
        if score >= 6:
            printr(f"[green][+] Master password Rating: {rating} [/green]")
        else:
            printr(f"[red][-] Master password Rating: {rating} [/red]")
            printr("[red][!] Please Try a Stronger Master![/red]")
            continue
        master_password_confirmation = getpass("Confirm Master password: ")
        if master_password == master_password_confirmation:
            return master_password
        printr("[red][-] Password Do Not Match [/red]")


def login():
    while True:
        email = input("email: ")
        master_password = getpass("Master Password: ")
        user_cred = db.get_user(email)
        result = db.get_vault_key_salt(user_cred['id'])
        vault_id = result['id']
        vault_key_salt = result['salt']
        user = User(user_cred['id'], user_cred['email'], user_cred['master_key'],
                    master_password, vault_id, vault_key_salt)
        is_authenticated = argon.authenticate_user(email, master_password, vault_key_salt, user.master_key)

        if not is_authenticated:
            printr("[red][-] Wrong Credentials Please Try Again [/red]")
            continue

        else:
            printr("[green][+] Authentication succeeded [/green]")
            user.vault_id = vault_id
            user.vault_key_salt = vault_key_salt
            return user


def generate_password(length=12):
    # Define the characters to use in the password
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_chars = string.punctuation

    # Combine all characters into one pool
    all_characters = uppercase_letters + lowercase_letters + digits + special_chars

    # Ensure at least one character from each category
    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(special_chars),
    ]

    # Fill the rest of the password length with random characters from all categories
    for _ in range(length - 4):
        password.append(random.choice(all_characters))

    # Shuffle the password characters to ensure unpredictability
    random.shuffle(password)

    # Convert the list of characters into a string
    password_str = ''.join(password)

    return password_str


# create a function that displays accounts in a table formattedd
def display_accounts(accounts):
    table_data = [
        [
            account.id,account.name,account.user_name,account.email,
            account.url,account.type,account.created_at,
            account.updated_at
        ]
        for account in accounts
    ]

    headers = [
                "ID", "Name", "Username", "Email", "URL",
                "Type", "Created At", "Updated At"
              ]

    print(tabulate(table_data,headers, tablefmt="fancy_grid"))


def copy_to_clipboard(password):
    """
    Copies the given password to the clipboard.

    Args:
        password (str): The password to copy to the clipboard.
    """
    try:
        pyperclip.copy(password)
        printr(f"[green][+] Copied to Clipboard [/green]")
    except Exception as e:
        print(f"An error occurred: {e}")






