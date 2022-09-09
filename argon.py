import binascii

import argon2


class argon:
    argon2Hasher=argon2.PasswordHasher(time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)


    def generate_derivation_key(email_mp):
        print(email_mp)

        dk=argon2.hash_password_raw(time_cost=16,memory_cost=2**15,parallelism=2,hash_len=32,
                                      password=email_mp.encode(),salt=b'some salt',type=argon2.low_level.Type.ID)
        print("Argon2 raw hash: ",dk)
        return binascii.hexlify(dk)
    def authenticate(hash,email_mp):
            try:
                x=argon.argon2Hasher.verify(hash,email_mp)
            except Exception as e:
                return False
            return x

    def generate_salted_dk(email_mp):
        salted_dk= argon.argon2Hasher.hash(email_mp)
        print("Argon2 hash (random salt):", hash)
        return salted_dk