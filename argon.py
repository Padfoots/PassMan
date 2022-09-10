import argon2
import base64


class argon:
    argon2Hasher=argon2.PasswordHasher(time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)

# for creating derivation key used to encrypt/decrypt the passwords in the vault
    def vault_key(email,master_password):
        master_key=argon.master_key(email,master_password)
        x=email+master_password+master_key

        derivation_key=argon2.hash_password_raw(time_cost=16,memory_cost=2**15,parallelism=2,hash_len=32,
                                      password=x.encode(),salt=b'some salt',type=argon2.low_level.Type.ID)

        return base64.urlsafe_b64encode(derivation_key)

    # use the master_key hash and the password entered by user to verify the log in
    def authenticate(master_key, password):
            try:
                x=argon.argon2Hasher.verify(master_key, password)
            except Exception as e:
                return False
            return x

# hashing the concatenation of the email and master password--> to produce master_key used for authentication
    def master_key(email,master_password):
        master_key= argon.argon2Hasher.hash(email+master_password)
        return master_key
