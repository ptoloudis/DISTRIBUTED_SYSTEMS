import socket
import select
from random import uniform

MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
MULTICAST_TTL = 2
UDP_PORT = 5005

find = False
serve = input("What do you want to ask? ")
for i in range(0, 3):
    print("Try to find the server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    sock.sendto(serve.encode(), (MCAST_GRP, MCAST_PORT))
    UDP_IP =  sock.getsockname()[0]
    sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock2.bind((UDP_IP, UDP_PORT))
    sock2.settimeout(uniform(1,4))
    try:
        dat, addr = sock2.recvfrom(50) # buffer size is 1024 bytes 
        find = True
        break  
    except socket.timeout:
        print("Write timeout on socket")
        continue

if find == False:
    print("Server not found")
    exit()

print(dat)
i = dat.find(b'_')
data = dat[:i].decode("utf-8")
z = int(data)+i+1
dat2 = dat[i+1:z]
print(dat2)
#print("Address:",addr[0]," received message: %s" % dat2.decode("utf-8"))