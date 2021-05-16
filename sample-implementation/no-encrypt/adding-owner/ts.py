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

# set up the socket with IPV4 and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

nonce_list = []
owners_list = {}

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
                msg = (cd_id, nonce2)
                O_t = bytes(f"{'OWN':<{HEADERSIZE}}", 'utf-8') + pickle.dumps(msg)
                conn.send(O_t)
                # print("O_t sent to CD")

            elif header == "OCD":
                # step 8 ----
                # recv O_cd
                O_cd = pickle.loads(data)

                assert(cd_id == O_cd[0])
                assert(nonceIncrement(nonce2) == O_cd[1])
                # print("Nonce 2 is verified from CD")
                owners_list[cd_id] = td_id
                # print("Added CD:TD to owners list")

                # step 9 ----
                msg = bytes(f"SUCCESS", 'utf-8')
                conn.send(msg)





if __name__ == '__main__':
    client_interaction()