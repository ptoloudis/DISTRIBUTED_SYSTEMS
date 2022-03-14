import socket
import select
from time import sleep
from random import uniform
import threading
from buffer_cl import *


MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
Ping_pong_port = 5007
IP_server = "";
MULTICAST_TTL = 2
UDP_PORT = 5005
find = False
Blabi = False
tmp = serveries()

def multicast_send(sock, serve):
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
            IP_server = addr[0]
            find = True
            break  
        except socket.timeout:
            print("Write timeout on socket")
            continue
    if find == False:
        print("Server not found")
        exit()
    i = dat.find(b'_')
    data = dat[:i].decode("utf-8")
    z = int(data)+i+1
    dat2 = dat[i+1:z]
    if dat2 == b'YES':
        print("Server found")
        tmp.add_id(serve, addr[0])
        return 1;
    else :
        print("Server not found")
        return 0;

def ping_pong():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sock.sendto("Pong".encode(), (IP_server, Ping_pong_port))
        UDP_IP =  sock.getsockname()[0]
        sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock2.bind((UDP_IP, Ping_pong_port))
        sock2.settimeout(uniform(1,5))
        try:
            dat, addr = sock2.recvfrom(50) # buffer size is 1024 bytes 
            find = True
            break  
        except socket.timeout:
            print("Write timeout on socket")
            continue
    if find == False:
        Blabi = True
        print("Server not found")
        exit()
    else:
        sleep(30)#5 seconds

def send(self,svcid, reqbuf, reqlen, resbuf, reslen):
    tmp = messeges(svcid, reqbuf, reqlen)
    id = tmp.return_id()
    self.send_buffer.add(tmp)
    tmp = self.re_buffer.get(id)
    resbuf = tmp.messege
    reslen = tmp.messege_length

def send_messeger():
    while True:
        tmp = send_buffer.get()
        #unpack(tmp.messege)
        #TODO: send messege
        #
        
        #TODO: receive messege
        #
        #pack the messege
        re_buffer.add(tmp)


## MAIN ##
send_buffer = buffer_send(10)
re_buffer = buffer_re(10)
id()
transport = False
x = threading.Thread(send_messeger)
x.start()
