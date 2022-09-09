import binascii

import argon2


class argon:
    argon2Hasher=argon2.PasswordHasher(time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)

# for creating the derivation key raw hash
    def a2bkdf(email_mp):

        derivation_key=argon2.hash_password_raw(time_cost=16,memory_cost=2**15,parallelism=2,hash_len=32,
                                      password=email_mp.encode(),salt=b'some salt',type=argon2.low_level.Type.ID)
        print("Argon2 raw hash: ",derivation_key)
        return binascii.hexlify(derivation_key)
    def authenticate(derivation_key,password):
            try:
                x=argon.argon2Hasher.verify(derivation_key,password)
            except Exception as e:
                return False
            return x

# for hashing passwords in the vault and verifying the master password whe logging in
    def a2_hash(password):
        hashed_password= argon.argon2Hasher.hash(password)
        print("Argon2 hash (random salt):", hashed_password)
        return hashed_password