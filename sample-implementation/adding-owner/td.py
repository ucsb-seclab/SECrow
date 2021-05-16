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

pubkey_cd = None

# try:
client, clientInfo = cd.accept()
while True:
    data = client.recv(size)
    total_bytes_recv += sys.getsizeof(data)
    header = (data[:HEADERSIZE]).decode().strip()
    data = data[HEADERSIZE:]
    if header:
        # print(f"Header: {header}")

        if header == 'ADD':   #add new owner
            # step 2 ----
            msg_recv = pickle.loads(data)
            pubkey_cd = rsa.PublicKey.load_pkcs1(msg_recv[0])
            paired_cd_id = msg_recv[1]

            # now make nonce1 and send it to CD
            nonce1 = secrets.token_hex(16)
            nonce_list.append(nonce1)
            msg = pickle.dumps(nonce1)
            client.send(msg)
            # total_bytes_sent += sys.getsizeof(msg)  
            # print("Sending nonce1 to CD.")

            # step 3 ----
            data = client.recv(size)
            # total_bytes_recv += sys.getsizeof(data)
            data = pickle.loads(data)
            nonce1_1 = data[0]
            verify_signature = rsa.verify(pickle.dumps(nonce1_1), data[1], pubkey_cd)
            # print("Signature for CD verified.")
            # nonce1_1 = pickle.loads(nonce1_1)
            assert(nonce1_1 == nonce1)
            # print("Local owner successfully added.")

            # step 6 ----
            # recv the O_t
            data = client.recv(size)
            # total_bytes_recv += sys.getsizeof(data)
            data = pickle.loads(data)
            pkey_cd_data = data[0]
            data = data[1]
            data = rsa.decrypt(data, privkey)
            data = pickle.loads(data)
            nonce2 = data[0]
            OT_k = data[1]
            # print("Paired CD id verified.")
            nonce3 = secrets.token_hex(16)
            nonce_list.append(nonce3)
            O_cd = (pkey_cd_data, nonce2, nonce3)
            O_cd = encrypt_message(O_cd, OT_k)

            # send O_cd to CD
            client.send(O_cd)
            # total_bytes_sent += sys.getsizeof(msg)

            # print(f"Total Bytes:\n\tSent: {total_bytes_sent}\n\tRecv: {total_bytes_recv}")
            # total_bytes_recv = total_bytes_sent = 0











        else:
            print(f"This message is not valid: {data}")

# except:	
#     print("Closing socket")
#     client.close()
#     s.close()
