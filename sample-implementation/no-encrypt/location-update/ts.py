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


def client_interaction():
    conn, addr = s.accept()
    while True:
        data = conn.recv(size)
        if data:
            header = (data[:HEADERSIZE]).decode().strip()
            data = data[HEADERSIZE:]

            if header == "HSK":
                # step 1 ----

                data = pickle.loads(data)
                # print(f"CD id: {data[1]}, TD id: {data[0]}")
                td_id = data[0]
                nonce_t = secrets.token_hex(16)
                nonce_list.append(nonce_t)
                nonce_c = secrets.token_hex(16)
                nonce_list.append(nonce_c)
                
                # make E_t
                E_t = pickle.dumps(nonce_t)
                conn.send(E_t)
                time.sleep(1)
                # print("Sent E_T")

                # make E_c
                E_c = pickle.dumps(nonce_c)
                conn.send(E_c)


            elif header == "LOC":
                # step 5 ----
                data = pickle.loads(data)
                L_data = data[0]
                S_t = data[1]
                L = L_data
                # assert(verify_sign == signature)
                # print("L is verified")
                # print("now checking S_t")
                S_t = pickle.loads(S_t)
                # assert(verify_sign == S_t[1])
                # print("S_t is verified")







if __name__ == '__main__':
    client_interaction()