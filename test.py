from random import randint
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    return s.getsockname()[0]

def get_free_port():
    while True:
        port = randint(3000, 5000 )
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not (sock.connect_ex(('127.0.0.1', port)) == 0):
            return port

Address = (get_ip(), get_free_port())
print("Address: " + str(Address))