import sys
import time

import mysql.connector
from mysql.connector import Error
from rich import print as printc
from rich.console import Console
import os
from dotenv import load_dotenv

load_dotenv()
console = Console()


# def db_connection():
#     try:
#         host = os.getenv('DB_HOST', 'localhost')  # Default to 'localhost' if not set
#         user = os.getenv('DB_USER', 'padfoot')  # Default to 'padfoot' if not set
#         password = os.getenv('DB_PASSWORD', 'fjfj')  # Default to 'fjfj' if not set
#         # Create the connection
#         conn = mysql.connector.connect(host=host,
#                                        user=user,
#                                        password=password)
#         return conn
#
#     except mysql.connector.Error as err:
#         console.print_exception(show_locals=True)
#         print(err)


def db_connection(retries=5, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            host = os.getenv('DB_HOST')  # Default to 'localhost' if not set
            user = os.getenv('DB_USER')  # Default to 'padfoot' if not set
            password = os.getenv('DB_PASSWORD')  # Default to 'fjfj' if not set

            # Attempt to create the connection
            conn = mysql.connector.connect(host=host, user=user, password=password)
            return conn

        except mysql.connector.Error as err:
            console.print(f"Connection failed on attempt {attempt + 1}: {err}")
            console.print_exception(show_locals=True)
            attempt += 1

            if attempt < retries:
                console.print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                console.print("[bold red]Max retries reached. Could not establish a connection.[/bold red]")

    return None

# def config():
#     db = db_connection()
#     cursor = db.cursor()
#
#     try:
#         # TODO: CHECK IF THE DATABASE EXITS IF IT DOES RETURN
#         exists = check_database_exists("PassMan")
#         if exists:
#             return
#         cursor.execute("DROP DATABASE IF EXISTS PassMan;")
#         cursor.execute(
#             '''
#                 CREATE DATABASE PassMan;
#             ''')
#     except Error:
#         printc("[red][!] Failed to create Database [/red")
#         console.print_exception(show_locals=True)
#         sys.exit(0)
#     printc("[green][+] Database created [/green]")
#     db.commit()
#
#     try:
#         query = '''
#                     CREATE TABLE PassMan.Users(
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         email VARCHAR(255) UNIQUE NOT NULL,
#                         master_key VARCHAR(255) NOT NULL
#                         );
#                 '''
#         cursor.execute(query)
#         query = '''
#                     CREATE TABLE PassMan.Vaults(
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         user_id INT NOT NULL,
#                         salt VARCHAR(255) NOT NULL,
#                         created_at TIMESTAMP NOT NULL
#                         DEFAULT CURRENT_TIMESTAMP,
#                         updated_at TIMESTAMP NOT NULL
#                         DEFAULT CURRENT_TIMESTAMP ON UPDATE
#                         CURRENT_TIMESTAMP,
#                         FOREIGN KEY (user_id) REFERENCES Users(id)
#                         );
#                 '''
#         cursor.execute(query)
#
#         query = '''
#                     CREATE TABLE PassMan.Accounts(
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         vault_id INT NOT NULL,
#                         name VARCHAR(255),
#                         user_name VARCHAR(255),
#                         email VARCHAR(255),
#                         password VARCHAR(255) NOT NULL ,
#                         url VARCHAR(255),
#                         type ENUM ('password','bank account','secure note','payment card'),
#                         aes_iv VARCHAR(255) UNIQUE NOT NULL,
#                         auth_tag VARCHAR(255)  UNIQUE NOT NULL,
#                         created_at TIMESTAMP NOT NULL
#                         DEFAULT CURRENT_TIMESTAMP,
#                         updated_at TIMESTAMP NOT NULL
#                         DEFAULT CURRENT_TIMESTAMP ON UPDATE
#                         CURRENT_TIMESTAMP,
#                         FOREIGN KEY (vault_id) REFERENCES Vaults(id)
#                         );
#                 '''
#         cursor.execute(query)
#         printc("[green][+] Tables created [/green]")
#     except Error:
#         printc("[red][!] Failed to create Database Tables")
#         console.print_exception(show_locals=True)
#         sys.exit(0)
#     finally:
#         cursor.close()
#         db.close()


def new_user(email, master_key):
    db = db_connection()
    cursor = db.cursor()
    query = '''
                INSERT INTO PassMan.Users (email, master_key) VALUES ( %s, %s);
            '''
    params = (email, master_key)
    try:
        cursor.execute(query, params)
        db.commit()
        last_inserted_id = cursor.lastrowid
        return last_inserted_id

    except Error:
        printc("[red][-] Failed to add User [/red]")
        console.print_exception(show_locals=True)
        return False
    finally:
        cursor.close()
        db.close()


def get_user(email):
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    query = '''
                SELECT id, email, master_key from PassMan.Users 
                WHERE email = %s ;
            '''
    params = (email,)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result:
        # parse the result into the User object and return it
        return result
    else:
        raise ValueError("could not find user check your credentials")


def new_vault(user_id, vault_key_salt):
    db = db_connection()
    cursor = db.cursor()
    query = ''' INSERT INTO PassMan.Vaults (user_id,salt)
                VALUES (%s, %s);
            '''
    params = (user_id, vault_key_salt)
    try:
        cursor.execute(query, params)
        db.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        db.close()


def get_vault_key_salt(user_id):
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    query = '''
                SELECT id, salt
                FROM PassMan.Vaults
                WHERE user_id = %s ;
            '''
    params = (user_id,)

    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result:
            return result
        else:
            printc("[red][-] could not find user vault [/red]")
    except Error as e:
        print(e)
    finally:
        cursor.close()
        db.close()


def new_account(account):
    db = db_connection()
    cursor = db.cursor()
    query = '''
                INSERT INTO PassMan.Accounts (vault_id, name, user_name, email,
                 `type`, password, url, aes_iv, auth_tag)
                 VALUES (%s, %s, %s, %s , %s, %s , %s, %s, %s);
            '''

    params = (account.vault_id, account.name,account.user_name, account.email,
              account.type,account.password,account.url, account.aes_iv, account.auth_tag)

    try:
        db = db_connection()
        cursor = db.cursor()
        cursor.execute(query, params)
        db.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        db.close()


def get_vault_accounts(vault_id):
    print("vault id: ", vault_id)
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    query = '''
                SELECT *
                FROM PassMan.Accounts
                WHERE vault_id = %s;
            '''
    params = (vault_id,)

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        if results:
            return results
        return None
    except Error as e:
        print(e)


def check_database_exists(db_name):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        result = cursor.fetchone()
        if result:
            return True
        return False
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


