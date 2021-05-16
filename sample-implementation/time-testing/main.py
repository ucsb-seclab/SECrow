from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.PublicKey import RSA
import Crypto.Hash.SHA256 as SHA256
import time

IV = 16 * b'\x00'
mode = AES.MODE_CBC
cipher = b'+jO1yukIAw8Vum1ifuTIGw=='
encryptor = AES.new(cipher, mode, IV=IV)
decryptor = AES.new(cipher, mode, IV=IV)

keyPair = RSA.generate(1024)
pubKey = keyPair.publickey()
encryptor_rsa = PKCS1_OAEP.new(pubKey)
decryptor_rsa = PKCS1_OAEP.new(keyPair)
signer = PKCS115_SigScheme(keyPair)
verifier = PKCS115_SigScheme(pubKey)


def pad(raw):
    padChar = b'\x00'
    padding_required = 16 - (len(raw) % 16)
    data = raw + padChar*padding_required
    return data

def unpad(raw):
    return raw.rstrip(b'\x00')

def encrypt_message(msg):
    return encryptor.encrypt(pad(msg))

def decrypt_message(msg):
    msg = unpad(decryptor.decrypt(msg))
    return msg

if __name__ == '__main__':
    msg = 64*"a"


    # test timing for symmetric encryption
    total_time = 0
    for i in range(20):
        t0 = time.time()
        for i in range(1000):
            encr = encrypt_message(msg.encode('utf-8'))
        t1 = time.time()
        total_time += (t1-t0)
    print(f"Asymmetric Encryption Time: {((total_time)/20)/1000}")


    # test timing for symmertric encrption
    total_time = 0
    encrypted_msg = encrypt_message(msg.encode('utf-8'))
    for i in range(20):
        t0 = time.time()
        for i in range(1000):
            decr = decrypt_message(encrypted_msg)
        t1 = time.time()
        total_time += (t1-t0)
    print(f"Asymmetric Decryption Time: {((total_time)/20)/1000}")

    # test timing for rsa sign
    total_time = 0
    signature = None
    hash_msg = SHA256.new(msg.encode('utf-8'))
    for i in range(20):
        t0 = time.time()
        for i in range(1000):
            signature = signer.sign(hash_msg)
        t1 = time.time()
        total_time += (t1-t0)
    print(f"RSA Sign Time: {((total_time)/20)/1000}")

    # test timing for rsa verification
    total_time = 0
    for i in range(20):
        t0 = time.time()
        for i in range(1000):
            verification_signature = verifier.verify(hash_msg, signature)
        t1 = time.time()
        total_time += (t1-t0)
    print(f"RSA Verify Time: {((total_time)/20)/1000}")

    # test timing for rsa encrypt
    total_time = 0
    encr = None
    for i in range(20):
        t0 = time.time()
        for i in range(1000):
            encr = encryptor_rsa.encrypt(msg.encode('utf-8'))
        t1 = time.time()
        total_time += (t1-t0)
    print(f"RSA Encrypt Time: {((total_time)/20)/1000}")

    # test timing for rsa decrypt
    total_time = 0
    for i in range(20):
        t0 = time.time()
        for i in range(1000):
            decr = decryptor_rsa.decrypt(encr)
        t1 = time.time()
        total_time += (t1-t0)
    print(f"RSA Decrypt Time: {((total_time)/20)/1000}")

