from rich import print as printr
import user
from user import display_accounts, generate_password, copy_to_clipboard


def main_menu():
    while True:
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user.register()
            printr("[blue] Please Login To Your Account [/blue]")
            logged_in_user = user.login()
            logged_in_menu(logged_in_user)
        elif choice == '2':
            logged_in_user = user.login()
            logged_in_menu(logged_in_user)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


def logged_in_menu(user):
    while True:
        print("1. Add New Account")
        print("2. Retrieve Account Data")
        print("3. Retrieve Account Password")
        print("4. Retrieve My Vault Accounts")
        print("5. Generate a New Password")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user.add_account()
            logged_in_menu(user)
        elif choice == '2':
            while True:
                account_name = input("account name: ")
                accounts = user.get_account(account_name)
                if accounts is None:
                    printr("[yellow][!] No accounts found in your vault with the given name [/yellow]")
                    choice = input("would you like to try Again [Y/n]").lower()
                    if choice == 'y':
                        continue
                    elif choice == 'n':
                        break
                display_accounts(accounts)
                # TODO: CREATE A MENU TO ASK IF YOU WANT TO EXIT OR RETRIEVE PASSWORD
                print("1. Search for another account")
                print("2. Retrieve account password")
                print("0. Back ")
                account_id = int(input("type account id to retrieve password: "))
                user.get_account_password(account_id)
        elif choice == '3':
            #TODO: CALL THE RETRIEVE ACCOUNT PASSWORD FUNCTION takes the name of the account
            # if multiple accounts with the same name display the results and let the user choose
            while True:
                account_name = input("account name: ")
                accounts = user.get_account(account_name)
                if accounts is None:
                    printr("[yellow][!] No accounts found in your vault with the given name [/yellow]")
                    printr("[blue] Would like to try Again? [Y/n] [/blue]")
                    choice = input(choice).lower()
                    if choice == 'y':
                        continue
                    elif choice == 'n':
                        break
                display_accounts(accounts)
                if len(accounts) > 1:
                    account_id = int(input("type account id to retrieve password: "))
                    user.get_account_password(account_id)
                    break
                else:
                    user.get_account_password(accounts[0].id)
                    break

        elif choice == '4':
            accounts = user.get_accounts()
            display_accounts(accounts)
            account_id = int(input("type account id to retrieve password: "))
            user.get_account_password(account_id)

        elif choice == '5':
            password_length = input("choose password length: ")
            password = generate_password(int(password_length))
            printr(f"[green][+] Generated password: [/green] [blue]{password}[/blue]")
            copy_to_clipboard(password)

        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == '__main__':
    main_menu()