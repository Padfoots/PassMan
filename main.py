import hashlib
import sys
from getpass import getpass
from rich import print as printr
from rich.console import Console
from argon import argon
from dbconfig import dbconfig

console = Console();

# functions definitions
def add_entry():
    name=input("name:")
    email=input("e-mail: ")
    password=getpass("password: ")
    url=input("url: ")
    username=input("username:")
    query="insert into passman.entries (name,email,password,url,username) values (%s,%s,%s,%s,%s)"
    hashed_password=argon.a2_hash(password)



# creating the tables


# run a query script to create tables
script = """
create database if not exists passman;
use passman;
create table vault(email text not null, master_key text not null,secret_key text not null);
create table records(email text not null, hashed_password text not null,username text,site_name text not null , url text not null);
"""

db = dbconfig()
cursor = db.cursor()
try:
    cursor.execute(script)
except Exception as e:
    printr("[red][!]error while creating tables")
    console.print_exception(show_locals=True)
    sys.exit(0)
printr("[green] [+] tables created succesfully")


# to retrieve the hash of the master password to authenticate the user


def get_master(email):
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("select master_key from passman.vault where email = %s ", (email,))
    mk = cursor.fetchall()
    cursor.close()
    db.close()
    return mk


# hash the master password to be saved in the db
def encrypt(password):
    hash = hashlib.sha256(password.encode()).hexdigest()
    return hash


def get_mp_hash(email):
    query = "select secret_key from passman.vault where email=%s"
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute(query, (email,))
    salted_dk = cursor.fetchone()
    cursor.close()
    db.close()
    return salted_dk[0]


################################main####################################################


# menu

printr("[blue] welcome to passman ")
choice = int(input("1-log-in to vault\n2-create a new vault\n"))


def login():
    email = input("email:")
    # send email to retrieve against it the hashed master password
    hashed_mp = get_master(email)
    print(hashed_mp)
    master_password = getpass("master password:")

    while not argon.authenticate(get_mp_hash(email), email + master_password):
        printr("[yellow] [-] wrong credentials please try again")
        email = input("email:")
        master_password = getpass("master password:")
    print("welcome back homie")


if choice == 1:
    login()
elif choice == 2:
    email = input("email:")
    flag = True;

    while flag:
        master_password = getpass("master password:")
        flag = master_password == "" or master_password != getpass("re-type:")
        if flag:
            print("password is empty or does not match! ")

    # encrypt the master password
    master_password_hash = argon.a2_hash(email+master_password)

    # derive secret key
    #ds = argon.a2_hash(vault_key, master_password)

    # store it in the vault database
    query = "insert into passman.vault (email,master_key,secret_key) values (%s,%s,%s)"
    val = (email, "hello",master_password_hash)
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute(query, val)
    db.commit()
    cursor.close()
    db.close()
    printr("[green] [+] your credentials has been saved please log-in to access your vault")
    login()

# prompt the user to choose register/sign in
# create the register menu
# enter email
# enter master password
# hash the master password
# derive a secret key
# store the (email,masterpass,secret key) into the vault table
# create the log in menu
# enter email
# enter master password
# check credentials in the vault table
# credentials if right enter the vault
# if wrong prompt the user again
# enter the vault
# prompt for a name of a website
# check the entries table against the name
# if name exists and unique dehash the password hash and copy it to clipboard
# if name exists but different emails display all emails with the name
# if name doesn't exist prompt user again for a name
