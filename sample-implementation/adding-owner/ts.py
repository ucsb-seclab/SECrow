import socket
import rsa
import secrets
import pickle
import time
from helpers import *

# hostname and port config
HOST = socket.gethostname() # could just be 127.0.0.1
PORT = 1234
HEADERSIZE = 10
size = 4096
OT_k = b'+jO1yukIAw8Vum1ifuTIGw=='

# set up the socket with IPV4 and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

nonce_list = []
owners_list = {}

with open('public_td.pem') as publicfile:
    pkeydata = publicfile.read()
    print("TD Public key loaded.")
pubkey_td = rsa.PublicKey.load_pkcs1(pkeydata)

with open('private_td.pem') as privatefile:
    keydata = privatefile.read()
    print("TD Private key loaded.")
privkey_td = rsa.PrivateKey.load_pkcs1(keydata,'PEM')

with open('public_cd.pem') as publicfile:
    pkeydata = publicfile.read()
    print("CD Public key loaded.")
pubkey_cd = rsa.PublicKey.load_pkcs1(pkeydata)


def client_interaction():
    conn, addr = s.accept()
    while True:
        data = conn.recv(size)
        if data:
            header = (data[:HEADERSIZE]).decode().strip()
            data = data[HEADERSIZE:]

            if header == "ADD":
                # step 4 ----
                msg_recv = pickle.loads(data)
                cd_id = msg_recv[0]
                td_id = msg_recv[1]
                nonce2 = secrets.token_hex(16)
                nonce_list.append(nonce2)
                msg = (nonce2, OT_k)
                O_t = bytes(f"{'OWN':<{HEADERSIZE}}", 'utf-8') + rsa.encrypt(pickle.dumps(msg), pubkey_td)
                conn.send(O_t)
                # print("O_t sent to CD")

            elif header == "OCD":
                # step 8 ----
                # recv O_cd
                O_cd = decrypt_message(data)
                # O_cd = pickle.loads(O_cd)

                assert(nonce2 == O_cd[1])
                # print("Nonce 2 is verified from CD")
                # owners_list[cd_id] = td_id
                # print("Added CD:TD to owners list")

                # step 9 ----
                msg = bytes(f"{'SUCCESS':<{HEADERSIZE}}", 'utf-8')
                conn.send(msg)





if __name__ == '__main__':
    client_interaction()