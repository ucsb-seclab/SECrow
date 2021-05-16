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
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)

nonce_list = []
HEADERSIZE = 10
paired_cd_id = ''

total_bytes_sent = 0
total_bytes_recv = 0

# try:
client, clientInfo = s.accept()
while True:
    data = client.recv(size)
    total_bytes_recv += sys.getsizeof(data)
    if data:

        # step 3
        nonce_t = data
        nonce_t = pickle.loads(nonce_t)
        # print(f"nonce_t is: {nonce_t}")
        
        # step 4
        S_t = (nonce_t)
        client.send(pickle.dumps(S_t))
        # total_bytes_sent += sys.getsizeof(pickle.dumps(S_t))

        # print(f"Total bytes:\n\tSent: {total_bytes_sent}\n\tRecv: {total_bytes_recv}")
        # total_bytes_sent = total_bytes_recv = 0


    else:
        print(f"This message is not valid: {data}")

# except:	
#     print("Closing socket")
#     client.close()
#     s.close()
