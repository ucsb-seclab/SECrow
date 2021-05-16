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
                data = pickle.loads(data)

                nonce = secrets.token_hex(16)
                msg = (Location(), nonce)
                msg = pickle.dumps(msg)
                conn.send(msg)




if __name__ == '__main__':
    client_interaction()