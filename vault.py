
from utils.db import db_connection
from pydantic import BaseModel
from datetime import datetime
from rich.console import Console
from tabulate import tabulate

console = Console()

class NewVault(BaseModel):
    id: int
    user_id: int
    name: str
    created_at: datetime
    updated_at: datetime




class Vault(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime



def new_vault(user_id):
    vault_name = input("vault name: ")
    db = db_connection()
    cursor = db.cursor()
    query = '''
                INSERT INTO PassMan.Vaults (user_id, name) VALUES ( %s, %s ) ;
            '''
    params = (user_id, vault_name)
    try:

        cursor.execute(query, params)
        db.commit()
        return True
    except Exception:
        console.print_exception(show_locals=True)
        return False
    finally:
        cursor.close()
        db.close()


def get_user_vaults(user_id):
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    query = '''
                SELECT id, name, created_at, updated_at
                FROM PassMan.Vaults 
                WHERE user_id = %s;
            '''
    params = (user_id,)
    try:

        cursor.execute(query, params)
        results = cursor.fetchall()
        vaults = [Vault(**row) for row in results]
        return vaults
    except Exception as e:
        console.print_exception(show_locals=True)
        return None
    finally:
        cursor.close()
        db.close()


def print_vaults(vaults):
    table_data = [
        [vault.id, vault.name, vault.created_at.strftime('%Y-%m-%d %H:%M:%S'),
         vault.updated_at.strftime('%Y-%m-%d %H:%M:%S')]
        for vault in vaults
    ]

    # Define headers
    headers = ["Vault ID", "Name", "Created At", "Updated At"]

    # Print table
    print(tabulate(table_data, headers, tablefmt="grid"))