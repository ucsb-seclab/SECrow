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
# td = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# td.connect((serverMACAddress, port))
cd_id = '1254d4e8219182b0392ac9ccff40e27e'
HEADERSIZE = 10
size = 4096

# Socket http settings
HOSTNAME = socket.gethostname()
PORT = 1234
ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts.connect((HOSTNAME, PORT))

def user_interaction():
    global total_bytes_recv, total_bytes_sent
    while True:
        text = input() # Note change to the old (Python 2) raw_input
        if text == "quit":
            break
        else:
            # step 1 ----
            
            t0 = time.time()
            msg = (cd_id, serverMACAddress)
            ts.send(bytes(f"{'HSK':<{HEADERSIZE}}", 'utf-8') + pickle.dumps(msg))

            data = ts.recv(size)

            data = pickle.loads(data)

            t1 = time.time()
            print(f"Total time: {t1-t0}")
            # print("Sent L and S_t to TS")






            





if __name__ == '__main__':
    user_interaction()
    s.close()