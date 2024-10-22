import binascii

from Crypto.Cipher import AES


def encrypt_AES_GCM(msg, aes_key):
    aesCipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(encrypted_password, nonce, authTag, aes_key):
    aesCipher = AES.new(aes_key, AES.MODE_GCM, binascii.unhexlify(nonce))
    decrypted_password = aesCipher.decrypt_and_verify(binascii.unhexlify(encrypted_password), binascii.unhexlify(authTag))
    return decrypted_password.decode('utf-8')

