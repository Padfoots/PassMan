# Password Manager Setup Documentation

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

1. **Git**: For cloning the repository.
2. **Python**: Version 3.6 or higher.
3. **Pip**: Python package installer (usually comes with Python).
4. **MySQL Database**: Make sure MySQL is installed and running.

## Setup Instructions

Follow these steps to set up the password manager application:

### 1. Clone the Repository

Open your terminal or command prompt and run the following command:

```bash
git clone https://github.com/Padfoots/Passman
```

### 2. Install Python and Pip

If Python is not already installed on your system, you can download it from the official website:

- [Download Python](https://www.python.org/downloads/)

After installation, verify Python and pip are installed correctly:

```bash
python --version
pip --version
```

### 3. Install MySQL Database

If MySQL is not installed, you can download it from the official website:

- [Download MySQL](https://dev.mysql.com/downloads/mysql/)

After installation, make sure the MySQL server is running. You can typically start it using:

```bash
# For Linux
sudo service mysql start

# For Windows, you may need to start it from the MySQL Workbench or Command Line
```

### 4. Install Requirements

Navigate to the cloned repository directory:

```bash
cd /PassMan
```



Then, install the required Python packages by running:

```bash
pip install -r requirements.txt
```

### 5. Edit the `.env` File for Database Credentials

1. Locate the `.env.example` file in the root of your project directory. This file contains example environment variables.
2. Copy or rename the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

3. Open the `.env` file in a text editor and update the database credentials as follows:

   ```plaintext
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=your_database_name
   ```

   Replace `your_username`, `your_password`, and `your_database_name` with your MySQL credentials.

### 6. Run the Application

Once you've completed the above steps, you can run the password manager application. The command will depend on how your application is structured, but it could look something like this:

```bash
python main.py
```
### 7. Create an Account

1. **Open the Application**: Launch your password manager application.
2. **Sign Up**: Navigate to the sign-up page.
3. **Enter Your Email**: Provide your email address.
4. **Choose a Master Password**: Create a strong master password. This password will be used to encrypt your vault and access your accounts.
5. **Confirm Your Password**: Re-enter your master password to confirm.

### 8. Create a Vault

1. After signing up, log in using your email and master password.
2. **Create a Vault**: Follow the on-screen instructions to create your vault. This is where all your accounts will be stored securely.

### 9. Add Accounts to Your Vault

1. Once your vault is created, navigate to the option for adding accounts.
2. **Enter Account Details**: Fill in the required information, such as:
   - Account Name (e.g., "Google", "Facebook")
   - Username or Email
   - Password
   - Any additional notes (optional)
3. **Save the Account**: Click on the save button to add the account to your vault.


