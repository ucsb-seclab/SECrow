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

with open('public_td.pem') as publicfile:
    pkeydata = publicfile.read()
    print("Public key loaded.")
pubkey = rsa.PublicKey.load_pkcs1(pkeydata)

with open('private_td.pem') as privatefile:
    keydata = privatefile.read()
    print("Private key loaded.")
privkey = rsa.PrivateKey.load_pkcs1(keydata,'PEM')

# try:
client, clientInfo = s.accept()
while True:
    data = client.recv(size)
    total_bytes_recv += sys.getsizeof(data)
    if data:

        # step 3
        nonce_t = rsa.decrypt(data, privkey)
        nonce_t = pickle.loads(nonce_t)
        print(f"nonce_t is: {nonce_t}")
        
        # step 4
        signature = rsa.sign(pickle.dumps(nonce_t), privkey, 'SHA-256')
        S_t = (nonce_t, signature)
        client.send(pickle.dumps(S_t))
        total_bytes_sent += sys.getsizeof(pickle.dumps(S_t))

        print(f"Total bytes:\n\tSent: {total_bytes_sent}\n\tRecv: {total_bytes_recv}")
        total_bytes_sent = total_bytes_recv = 0


    else:
        print(f"This message is not valid: {data}")

# except:	
#     print("Closing socket")
#     client.close()
#     s.close()
