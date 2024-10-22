-- init.sql

-- Check if the database exists and create it if it doesn't
CREATE DATABASE IF NOT EXISTS PassMan;
GRANT ALL PRIVILEGES ON PassMan.* TO 'passman_admin'@'%';
FLUSH PRIVILEGES;
USE PassMan;

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    master_key VARCHAR(255) NOT NULL
);

-- Create Vaults table
CREATE TABLE IF NOT EXISTS Vaults (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    salt VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create Accounts table
CREATE TABLE IF NOT EXISTS Accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vault_id INT NOT NULL,
    name VARCHAR(255),
    user_name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    url VARCHAR(255),
    type ENUM('password', 'bank account', 'secure note', 'payment card'),
    aes_iv VARCHAR(255) UNIQUE NOT NULL,
    auth_tag VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (vault_id) REFERENCES Vaults(id)
);
