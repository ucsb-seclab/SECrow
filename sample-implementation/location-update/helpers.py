import json
import sys

HEADERSIZE = 10

class UpdateToken:
    def __init__(self, cd_id, nonce2, nonce1):
        self.nonce2 = nonce2
        self.nonce1 = nonce1
        self.cd_id = cd_id

class Location:
    def __init__(self, latitude=-31.863, longitude=11.56):
        self.latitude = latitude
        self.longitude = longitude
        
class LocationToken:
    def __init__(self, nonce_c, location):
        self.nonce_c = nonce_c
        self.location = location

def nonceIncrement(nonce):
    return str(hex(int(nonce, base=16) + 1))

def dump(data):
    return bytes(json.dumps(data), 'utf-8')

def load(dump):
    return json.loads(dump).decode()

def recvData(conn):
    data = b""
    size = -1
    while True:
        packet = conn.recv(4096)
        if size == -1:
            size = int((packet[:HEADERSIZE]).decode().strip())
            packet = packet[HEADERSIZE:]
        print("received data")
        if not packet: break
        data += packet
        if sys.getsizeof(data) >= size: break
    return data[HEADERSIZE:]