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
            nonce = pickle.loads(nonce)

            # step 3
            msg = (nonce, b'+jO1yukIAw8Vum1ifuTIGw==')
            R = bytes(f"{'FIN':<{HEADERSIZE}}", 'utf-8') + pickle.dumps(msg)
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

