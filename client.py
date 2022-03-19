import socket
from time import sleep
from random import uniform
import threading
from library.buffer import *
from library.messages import *
from library.services import *
from library.id import *

PORT_MESS = 12000
MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
Ping_pong_port = 5007
Ping_pong_port2 = 5008
IP_server = None
MULTICAST_TTL = 2
TTL = 5
UDP_PORT = 5005
Damage = False
servs = services()
id = Id()

def multicast_send( serve:str):
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
        return 1
    else :
        print("Server not found")
        return 0

def ping_pong():
    while True:
        find = False
        for i in range(0, 20):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            sock.sendto("Pong".encode(), (IP_server, Ping_pong_port))
            UDP_IP =  sock.getsockname()[0]
            sock2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock2.bind((UDP_IP, Ping_pong_port2))
            sock2.settimeout(uniform(1,4))
            try:
                dat, addr = sock2.recvfrom(50) # buffer size is 1024 bytes 
                print("UP")
                IP_server = addr[0]
                find = True
                break   
            except socket.timeout:
                continue
        
        if find == False:
            Damage = True
            print("Server Down")
            exit()
        else:
            sleep(5)#5 seconds

def send(svcid, reqbuf):
    global id
    tmp = myMes(svcid, reqbuf, id)
    id = tmp.return_id()
    send_buffer.add(tmp)
    tmp = re_buffer.get(id)
    return tmp.messege
    
def send_messeger():
    while True:
        tmp:myMes = send_buffer.get()
        while tmp == None:
            tmp = send_buffer.get()
        
        message_send = "%d_1_%d_%d_%s" %(tmp.return_message_length(), tmp.return_checksum(), tmp.return_id(), tmp.return_message()) 
        if (servs.get_id(tmp.destination) == 0 ):
            if(multicast_send(chr(tmp.destination)) == 0):
                print("Server not found")
                return -1
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, TTL)
        x = threading.Thread(ping_pong)
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
        z.kill()

def send_to_server(file_name:str, svrid:int):
    file = open(file_name, "rb")
    while True:
        data = file.readline(1024)
        if not data:
            break
        data = data.decode("utf-8")
        data.replace('\n',"")
        send(svrid, data)
    file.close()

## MAIN ##

send_buffer = buffer_send(10)
re_buffer = buffer_re(10)
transport = False
i = 0
z= [0,0,0,0,0,0,0,0,0,0]

x = threading.Thread(target = send_messeger)
x.start()
for i in range(0, 10):
    file_name = input("Enter file name: ")
    if file_name == "exit" or Damage == True:
        break
    while True:
        svrid = int(input("Enter server id: "))
        if (svrid ):
            break
        else:
            print("Enter a valid server id")
    z[i]= threading.Thread(send_to_server(file_name, svrid))
    z[i].start()

while True:
    
    if (Damage):
        print("Fail to connect to server")
        print("Server Down")
        x.kill()
        exit() 
        for k in range(0, i):
            z[k].kill()
    