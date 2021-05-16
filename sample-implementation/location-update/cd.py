import bluetooth
import rsa
import sys
import socket
import pickle
import time
import threading
from helpers import *

serverMACAddress = 'B8:27:EB:BC:FD:8B'
port = 3
td = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
td.connect((serverMACAddress, port))
cd_id = '1254d4e8219182b0392ac9ccff40e27e'
HEADERSIZE = 10
size = 4096

# Socket http settings
HOSTNAME = socket.gethostname()
PORT = 1234
ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts.connect((HOSTNAME, PORT))

total_bytes_recv = 0
total_bytes_sent = 0

with open('public_td.pem') as publicfile:
    pkeydata = publicfile.read()
    print("TD Public key loaded.")
pubkey_td = rsa.PublicKey.load_pkcs1(pkeydata)

with open('public_cd.pem') as publicfile:
    pkeydata = publicfile.read()
    print("CD Public key loaded.")
pubkey_cd = rsa.PublicKey.load_pkcs1(pkeydata)

with open('private_cd.pem') as privatefile:
    keydata = privatefile.read()
    print("Private key loaded.")
privkey_cd = rsa.PrivateKey.load_pkcs1(keydata,'PEM')


def user_interaction():
    global total_bytes_recv, total_bytes_sent
    while True:
        text = input() # Note change to the old (Python 2) raw_input
        if text == "quit":
            break
        else:
            # step 1 ----
            # send ID of the CD
            t0 = time.time()
            msg = (serverMACAddress, cd_id)
            msg = bytes(f"{'HSK':<{HEADERSIZE}}", 'utf-8') + pickle.dumps(msg)
            ts.send(msg)
            # print("Sent HSK to TS")
            
            #step 2 ----
            # receive E_t and E_c
            E_t = ts.recv(size)
            # time.sleep(1)
            E_c = ts.recv(size)

            nonce_c = rsa.decrypt(E_c, privkey_cd)
            nonce_c = pickle.loads(nonce_c)
            # print(f"Nonce C is: {nonce_c}")


            # step 3 ----
            # send E_t to TD
            td.send(E_t)

            # step 4 ----
            # receive Sign token from TD
            S_t = td.recv(size)
            # print("Received S_t from TD")

            # step 5 ----
            # send update token to TD
            L = LocationToken(nonce_c, Location())
            signature = rsa.sign(pickle.dumps(L), privkey_cd, 'SHA-256')
            msg = ((L, signature), S_t)
            msg = bytes(f"{'LOC':<{HEADERSIZE}}", 'utf-8') + pickle.dumps(msg)
            ts.send(msg)
            t1 = time.time()
            print(f"Total time: {t1-t0}")
            # print("Sent L and S_t to TS")






            





if __name__ == '__main__':
    user_interaction()
    s.close()