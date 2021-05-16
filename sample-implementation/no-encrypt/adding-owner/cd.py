import bluetooth
import rsa
import sys
import socket
import pickle
import time
from helpers import *

# hostname and port config
serverMACAddress = 'B8:27:EB:BC:FD:8B'
port = 3
td = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
td.connect((serverMACAddress, port))
cd_id = '1254d4e8219182b0392ac9ccff40e27e'
HEADERSIZE = 10
size = 4096
total_bytes_sent = 0
total_bytes_recv = 0

# Socket http settings
HOSTNAME = socket.gethostname()
PORT = 1234
ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts.connect((HOSTNAME, PORT))


def user_interaction():
    global total_bytes_recv
    global total_bytes_sent
    while True:
        text = input() # Note change to the old (Python 2) raw_input
        if text == "quit":
            break
        else:
            t0 = time.time()
            # step 1 --------
            add_msg = cd_id
            msg = bytes(f"{'ADD':<{HEADERSIZE}}", 'utf-8') + pickle.dumps(add_msg)
            td.send(msg)
            # total_bytes_sent += sys.getsizeof(msg)
            # print("Sent add request to TD.")
            
            # step 3 --------
            msg = td.recv(size)
            # total_bytes_recv += sys.getsizeof(msg)
            nonce1 = pickle.loads(msg)
            # do nonce + 1
            # sign with private key
            nonce1_1 = pickle.dumps(nonceIncrement(nonce1))
            # build msg to send
            td.send(nonce1_1)
            # total_bytes_sent += sys.getsizeof(pickle.dumps(msg))
            # print("Sent nonce1+1 to TD.")

            # step 4 -------
            # send msg to TS
            msg = (cd_id, serverMACAddress)
            msg = bytes(f"{'ADD':<{HEADERSIZE}}", 'utf-8') + pickle.dumps(msg)
            ts.send(msg)
            # total_bytes_sent += sys.getsizeof(msg)
            
            # step 6 -------
            data = ts.recv(size)
            # total_bytes_recv += sys.getsizeof(data)
            header = data[:HEADERSIZE].decode().strip()
            if header != "OWN":
                print("OWN: incorrect header")
                break
            O_t = data[HEADERSIZE:]
            # send to TD 
            td.send(O_t)
            # total_bytes_sent += sys.getsizeof(O_t)

            # step 7 -------
            # recv O_cd from TD
            O_cd = td.recv(size)
            # total_bytes_recv += sys.getsizeof(O_cd)
            # send O_cd and O_t to TS

            # sending O_cd 
            O_cd = bytes(f"{'OCD':<{HEADERSIZE}}", 'utf-8') + O_cd
            ts.send(O_cd)
            # total_bytes_sent += sys.getsizeof(O_cd)

            # recv suceess/fail
            data = ts.recv(size)
            # total_bytes_recv += sys.getsizeof(data)
            if data.decode().strip() != "SUCCESS":
                print("Add failed from TS.")
            # else:
            #     print("Add successful from TS.")
            
            t1 = time.time()
            print(f"Total time: {t1-t0}")
            # print(f"Total Bytes:\n\tSent: {total_bytes_sent}\n\tRecv: {total_bytes_recv}")
            # total_bytes_recv = total_bytes_sent = 0




if __name__ == '__main__':
    user_interaction()
    s.close()

