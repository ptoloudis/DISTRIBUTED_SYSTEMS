#
#Team : 1
#Names : Apostolopoulou Ioanna & Toloudis Panagiotis
#AEM : 03121 & 02995
#

import socket
from random import uniform
import threading
import struct


MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
MULTICAST_TTL = 2
TTL = 5
TCP_PORT = 5005


def multicast_send(serve:str):
    find = False
    for i in range(0, 3):
        print("Try to find the server")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sock.sendto(serve.encode(), (MCAST_GRP, MCAST_PORT))
        sock.settimeout(uniform(3,6))
        try:
            addr = sock.recvfrom(50) # buffer size is 1024 bytes 
            IP_server = addr[0]
            find = True
            break  
        except socket.timeout:
            print("Write timeout on socket")
            continue
    if find == False:
        print("Server not found")
        exit()
    print(addr)
    return (IP_server)
    
    # if data == 49 :
    #     print("Server found")
    #     return 1

def multicast_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            print("Received message:", data.decode()) 
            sock.sendto(data, addr)
        except:
            continue

# def Process():
#     GM = multicast_send(1)


# def TCP_manager():
    
# def Manager():





def TCP_process(GM):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((GM, TCP_PORT))
    while True:
        data = input("Enter the message: ")
        sock.send(data.encode())
        data = sock.recv(1024)
        print(data.decode())


def Manager():
    TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_socket.bind(('10.97.4.90  ', TCP_PORT))
    TCP_socket.listen(3)

    conn, addr = TCP_socket.accept()
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data: break
        print(data.decode())
        conn.send(data)
    conn.close()


def Process():
    GM = multicast_send('1')
    print("HEY THERE")
    TCP_process(GM)

def GroupManager():
    threading.Thread(target = multicast_receiver).start()
    while True:
        Manager()
    















    
def main():
    threading.Thread(target = GroupManager).start()
    while True:
        Process()


if __name__ == '__main__':
    main()