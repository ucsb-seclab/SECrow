import sys

def nonceIncrement(nonce):
    return str(hex(int(nonce, base=16) + 1))