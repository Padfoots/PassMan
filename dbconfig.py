# connecting with mysql database
import mysql.connector
from rich.console import Console

console=Console()

def dbconfig():
    try:
        db=mysql.connector.connect(
            host="localhost",
            user="root",
            password="hewhomustnotbenamed.n461n1")
    except Exception as e:
        console.print_exception(show_locals=True)
    return db
