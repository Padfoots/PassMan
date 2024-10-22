import base64
import binascii

import argon2
from aes import encrypt_AES_GCM, decrypt_AES_GCM
argon2Hasher = argon2.PasswordHasher(
    time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)


def parse_argon2_hash(argon2_hash):
    # Split the hash into its components
    parts = argon2_hash.split('$')

    # Extract the components
    algorithm = parts[1]
    version = parts[2]

    # Extract parameters (memory_cost, time_cost, parallelism)
    params = parts[3].split(',')
    memory_cost = int(params[0].split('=')[1])
    time_cost = int(params[1].split('=')[1])
    parallelism = int(params[2].split('=')[1])

    salt = parts[4]
    hash = parts[5]

    return {
        'algorithm': algorithm,
        'version': version,
        'memory_cost': memory_cost,
        'time_cost': time_cost,
        'parallelism': parallelism,
        'salt': salt,
        'hash': hash
    }


def generate_master_key(email, master_password):
    vault_key_hash, vault_key_salt = generate_vault_key(email, master_password)
    master_key_combination = vault_key_hash + master_password
    # TODO: REMOVE THE VAULT KEY HASH IN THE RETURN STATEMENT
    return argon2Hasher.hash(master_key_combination) , vault_key_salt, vault_key_hash


def generate_vault_key(email, master_password):
    vault_key_combination = email + ':' + master_password
    argon_vault_key_hash = argon2Hasher.hash(vault_key_combination)
    parsed_hash = parse_argon2_hash(argon_vault_key_hash)
    vault_key_salt = parsed_hash['salt']
    vault_key_hash = parsed_hash['hash']
    return vault_key_hash, vault_key_salt


def compute_vault_key(email, master_password, salt_str):
    salt_bytes = base64.urlsafe_b64decode(salt_str + '==')
    vault_key_combination = email + ':' + master_password
    argon_vault_key_hash = argon2Hasher.hash(vault_key_combination, salt=salt_bytes)
    parsed_hash = parse_argon2_hash(argon_vault_key_hash)
    vault_key_hash = parsed_hash['hash']
    return vault_key_hash


def authenticate_user(email, master_password, vault_key_salt, master_key_hash):
    vault_key_hash = compute_vault_key(email, master_password, vault_key_salt)
    key_combination = vault_key_hash + master_password
    try:
        argon2Hasher.verify(master_key_hash, key_combination)
        return True
    except Exception as e:
        return False




# TESTING

# email = "youssefsamir2000@gmail.com"
# master_password = "fjfj"
#
# # the vault key_salt is used to generate the same hash again when authenticating a user
# master_key_hash, vault_key_salt, vault_key_hash = generate_master_key(email, master_password)
# print("master_key_hash: ", master_key_hash)
# print("vault_key_salt: ", vault_key_salt)
#
# # call the compute vault key with the vault key salt
# vault_key_hash_computed = compute_vault_key(email, master_password,vault_key_salt)
#
#
# authenticate_user(email, master_password, vault_key_salt, master_key_hash)
#
# # now we want to test encrypting and decrypting using aes
# message = b"hi taha"
# aes_key = compute_vault_key(email, master_password,vault_key_salt)
# aes_key_decoded = base64.urlsafe_b64decode(aes_key + '==')
# encryptedMsg = encrypt_AES_GCM(message,aes_key_decoded)
# print("encryptedMsg", {
#     'ciphertext': binascii.hexlify(encryptedMsg[0]),
#     'aesIV': binascii.hexlify(encryptedMsg[1]),
#     'authTag': binascii.hexlify(encryptedMsg[2])
# })
#
 #decryptedMsg = decrypt_AES_GCM(encryptedMsg, aes_key_decoded)
# print("decrypted message: ", decryptedMsg)