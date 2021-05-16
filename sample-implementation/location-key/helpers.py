import sys
import pickle
from Crypto.Cipher import AES

IV = 16 * b'\x00'
mode = AES.MODE_CBC
L_td = b'+jO1yukIAw8Vum1ifuTIGw=='
encryptor = AES.new(L_td, mode, IV=IV)

def nonceIncrement(nonce):
    return str(hex(int(nonce, base=16) + 1))

def pad(raw):
    padChar = b'\x00'
    padding_required = 16 - (len(raw) % 16)
    data = raw + padChar*padding_required
    return data

def unpad(raw):
    return raw.rstrip(b'\x00')

def encrypt_message(msg):
    msg = pickle.dumps(msg)
    return encryptor.encrypt(pad(msg))

def decrypt_message(msg):
    msg = unpad(encryptor.decrypt(msg))
    return pickle.loads(msg)