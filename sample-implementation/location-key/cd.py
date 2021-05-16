import bluetooth
import rsa
import sys
import socket
import pickle
import time

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

# # Socket http settings
# HOSTNAME = socket.gethostname()
# PORT = 1234
# ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ts.connect((HOSTNAME, PORT))

with open('public_td.pem') as publicfile:
    pkeydata = publicfile.read()
    print("TD Public key loaded.")
pubkey_td = rsa.PublicKey.load_pkcs1(pkeydata)

with open('public_cd.pem') as publicfile:
    pkeydata_cd = publicfile.read()
    print("CD Public key loaded.")
pubkey_cd = rsa.PublicKey.load_pkcs1(pkeydata_cd)

with open('private_cd.pem') as privatefile:
    keydata = privatefile.read()
    print("Private key loaded.")
privkey_cd = rsa.PrivateKey.load_pkcs1(keydata,'PEM')


def user_interaction():
    global total_bytes_recv
    global total_bytes_sent
    while True:
        text = input() # Note change to the old (Python 2) raw_input
        if text == "quit":
            break
        else:
            t0 = time.time()

            # step 1
            td.send(bytes(f"{'LUP':<{HEADERSIZE}}", 'utf-8'))

            nonce = td.recv(size)
            nonce = rsa.decrypt(nonce, privkey_cd)
            nonce = pickle.loads(nonce)

            # step 3
            msg = (nonce, b'+jO1yukIAw8Vum1ifuTIGw==')
            R = bytes(f"{'FIN':<{HEADERSIZE}}", 'utf-8') + rsa.encrypt(pickle.dumps(msg), pubkey_td)
            td.send(R)

            # step 4
            ack = td.recv(size)
            assert(ack.decode() == "ACK")




            
            t1 = time.time()
            print(f"Total time: {t1-t0}")
            # print(f"Total Bytes:\n\tSent: {total_bytes_sent}\n\tRecv: {total_bytes_recv}")
            # total_bytes_recv = total_bytes_sent = 0




if __name__ == '__main__':
    user_interaction()

