import cli
from utils import db
from rich import print as printr
printr("[cyan]*[/cyan]"*60 + "[blue]PassMan[/blue]" + "[cyan]*[/cyan]"*60)
# first we create the database
# db.config()

# call the main menu
cli.main_menu()