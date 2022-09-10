import hashlib
import sys
from getpass import getpass
from rich import print as printr
from rich.console import Console
from argon import argon
from dbconfig import dbconfig
from cryptography.fernet import Fernet

console = Console();

# functions definitions
def add_entry(mail,master_password):
    name=input("name:")
    email=input("e-mail: ")
    password=getpass("password: ")
    url=input("url: ")
    username=input("username:")
    query="insert into passman.records (site_name,email,hashed_password,url,username) values (%s,%s,%s,%s,%s)"
    vault_key=argon.vault_key(mail,master_password)
    encry_pass=Fernet(vault_key).encrypt(password.encode())
    print("encrypted password ", encry_pass)
    decry_pass=Fernet(vault_key).decrypt(encry_pass).decode()
    print("decrypted password: " ,decry_pass)

    val=name,email,encry_pass,url,username
    db=dbconfig()
    cursor=db.cursor()
    cursor.execute(query,val)
    printr("[green][+] entry is added succesfully")
    cursor.close()
    db.commit()
    db.close()



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

printr(
"""[blue]**************************************************************** welcome to passman ****************************************************************""")
choice = int(input("1-log-in to vault\n2-create a new vault\n"))


def login():
    email = input("email:")
    # send email to retrieve against it the hashed master password
    hashed_mp = get_master(email)
    print(hashed_mp)
    master_password = getpass("master password:")

    while not argon.authenticate(get_mp_hash(email),email+master_password):
        printr("[yellow] [-] wrong credentials please try again")
        email = input("email:")
        master_password = getpass("master password:")
    print("welcome back homie")
    input("1-enter a new entry")
    add_entry(email,master_password)


def register():
    global db, cursor
    email = input("email:")
    flag = True;
    while flag:
        master_password = getpass("master password:")
        flag = master_password == "" or master_password != getpass("re-type:")
        if flag:
            print("password is empty or does not match! ")
    master_key = argon.master_key(email, master_password)
    # store it in the vault database
    query = "insert into passman.vault (email,master_key,secret_key) values (%s,%s,%s)"
    val = (email, "hello", master_key)
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute(query, val)
    db.commit()
    cursor.close()
    db.close()
    printr("[green] [+] your credentials has been saved please log-in to access your vault")
    login()


if choice == 1:
    login()
elif choice == 2:
    register()
