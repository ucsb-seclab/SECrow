import bluetooth
import secrets
import Crypto
import rsa
import pickle
import sys
import time

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

with open('public_cd.pem') as publicfile:
    pkeydata = publicfile.read()
    print("Public key loaded.")
pubkey_cd = rsa.PublicKey.load_pkcs1(pkeydata)

with open('private_td.pem') as privatefile:
    keydata = privatefile.read()
    print("Private key loaded.")
privkey = rsa.PrivateKey.load_pkcs1(keydata,'PEM')


# try:
client, clientInfo = cd.accept()
while True:
    data = client.recv(size)
    total_bytes_recv += sys.getsizeof(data)
    header = (data[:HEADERSIZE]).decode().strip()
    data = data[HEADERSIZE:]
    if header:
        # print(f"Header: {header}")

        if header == "LUP":
            # step 2
            nonce = secrets.token_hex(16)
            encrypted = rsa.encrypt(pickle.dumps(nonce), pubkey_cd)
            client.send(encrypted)

        elif header == "FIN":
            data = rsa.decrypt(data, privkey)
            data = pickle.loads(data)
            nonce_recv = data[0]
            L_td = data[1]
            assert(nonce == nonce_recv)
            client.send(bytes("ACK", "utf-8"))

        else:
            print(f"This message is not valid: {data}")
            