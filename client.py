from ast import While
from email import message
from lib2to3.pytree import NodePattern
import socket
from time import sleep
from random import uniform
import threading
from library.buffer import *
from library.messege import *
from library.serveries import *


PORT_MESS = 5010
MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
Ping_pong_port = 5007
Ping_pong_port2 = 5008
IP_server = None
MULTICAST_TTL = 2
TTL = 5
UDP_PORT = 5005
Blabi = False
servs = serveries()
send_buffer = buffer_send(10)
re_buffer = buffer_re(10)

def multicast_send(sock, serve:str):
    for i in range(0, 3):
        print("Try to find the server")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sock.sendto(serve.encode(), (MCAST_GRP, MCAST_PORT))
        UDP_IP =  sock.getsockname()[0]
        sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock2.bind((UDP_IP, UDP_PORT))
        sock2.settimeout(uniform(3,6))
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
    print(dat[4])
    data = dat[4] 
    if data == 49 :
        print("Server found")
        servs.add_id(serve, addr[0], addr[1])
        return 1;
    else :
        print("Server not found")
        return 0;

def ping_pong():
    while True:
        find = False
        for i in range(0, 3):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            sock.sendto(b"Pong", (IP_server, Ping_pong_port))
            UDP_IP =  sock.getsockname()[0]
            sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock2.bind((UDP_IP, Ping_pong_port2))
            sock2.settimeout(uniform(1,4))
            try:
                dat, addr = sock2.recvfrom(50) # buffer size is 1024 bytes 
                print("UP")
                find = True
                break   
            except socket.timeout:
                continue
        
        if find == False:
            Blabi = True
            print("Server Down")
            exit()
        else:
            sleep(5)#5 seconds

def send(svcid, reqbuf, reqlen):
    tmp = messeges(svcid, reqbuf, reqlen)
    id = tmp.return_id()
    send_buffer.add(tmp)
    tmp = re_buffer.get(id)
    return tmp

def send_messeger():
    while True:
        tmp = send_buffer.get()
        mess_len = len(tmp.messege).encode()

        message_send = mess_len +'_1_'+ tmp.checksum.encode() +tmp.return_id().encode()+'_'+tmp.messege
        if (servs.get_id(tmp.destination) == 0 ):
            if(multicast_send(tmp.destination) == 0):
                print("Server not found")
                return -1;
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, TTL)
        for i in range (0, 5):
            sock.settimeout(uniform(3,6))
            try:
                sock.sendto(message_send.encode(), (servs.get_ip(),PORT_MESS))
                if (sock.recv(7) == "1_1_1"):
                    break
                else :
                    continue
            except socket.timeout:
                continue
        resive = sock.recv(70)
        i = resive.find(b'_')
        data =resive[:i].decode("utf-8")
        z = int(data)
        dat2 = resive[i+3:].find(b'_')
        check = int(resive[i+3:i+3+dat2].decode("utf-8"))
        mess = resive[i+3+dat2+3:].decode("utf-8")
        if (check == hash(mess)):
            sock.sendto("1_1_1".encode(), (servs.get_ip(),PORT_MESS))
            if re_buffer.find(mess):
                re_buffer.add(mess) 
        else:
            sock.sendto("1_1_0".encode(), (servs.get_ip(),PORT_MESS))

 
## MAIN ##


transport = False
x = threading.Thread(target=send_messeger)
z = threading.Thread(target=ping_pong)
x.start()
z.start()

k = input("Enter the service id: ")
j = input("Enter the request: ")

print(send(k, j, len(j)))
while True:
    if (Blabi):
        print("Fail to connect to server")
        print("Server Down")
        x.kill()
        z.kill()
        exit() 