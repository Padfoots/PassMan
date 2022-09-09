import sys

import dbconfig
from rich import print as printr
from rich.console import Console
console=Console();

def config():

# connect with the database

    db=dbconfig()
    cursor=db.cursor()

    # run a query script to create tables
    script="""
    create database if not exists passman;
    use passman;
    create table vault(email text not null, master_key text not null,secret_key text not null);
    create table records(email text not null, hashed_password text not null,username text,site_name text not null , url text not null);
    """
    try:
        cursor.execute(script)
    except Exception as e:
        printr("[red][!]error while creating tables")
        console.print_exception(show_locals=True)
        sys.exit(0)
    print("[green] [+] [/green] tables created succesfully")
    return db
