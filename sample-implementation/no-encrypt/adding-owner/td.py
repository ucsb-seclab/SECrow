import bluetooth
import secrets
import Crypto
import rsa
import pickle
import sys
import time
from helpers import *

hostMACAddress = 'B8:27:EB:BC:FD:8B' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 4096
cd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
cd.bind((hostMACAddress, port))
cd.listen(backlog)

nonce_list = []
HEADERSIZE = 10
paired_cd_id = ''

total_bytes = 0

# try:
client, clientInfo = cd.accept()
while True:
    data = client.recv(size)
    total_bytes += sys.getsizeof(data)
    header = (data[:HEADERSIZE]).decode().strip()
    data = data[HEADERSIZE:]
    if header:
        print(f"Header: {header}")

        if header == 'ADD':   #add new owner
            # step 2 ----
            msg_recv = pickle.loads(data)
            paired_cd_id = msg_recv

            # now make nonce1 and send it to CD
            nonce1 = secrets.token_hex(16)
            nonce_list.append(nonce1)
            msg = pickle.dumps(nonce1)
            client.send(msg)
            # print("Sending nonce1 to CD.")

            # step 3 ----
            data = client.recv(size)
            data = pickle.loads(data)
            nonce1_1 = data
            assert(nonce1_1 == nonceIncrement(nonce1))
            # print("Local owner successfully added.")

            # step 6 ----
            # recv the O_t
            data = client.recv(size)
            data = pickle.loads(data)
            print(data)
            print(paired_cd_id)
            assert(data[0] == paired_cd_id)
            # print("Paired CD id verified.")
            nonce2_1 = nonceIncrement(data[1])
            msg = (paired_cd_id, nonce2_1)
            msg = pickle.dumps(msg)
            # send O_cd to CD
            client.send(msg)













        else:
            print(f"This message is not valid: {data}")

# except:	
#     print("Closing socket")
#     client.close()
#     s.close()
