#
#Team : 1
#Names : Apostolopoulou Ioanna & Toloudis Panagiotis
#AEM : 03121 & 02995
#

import socket
from random import uniform
import threading
import struct
import sys

MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
IP_Manager = None
MULTICAST_TTL = 2
TTL = 5
TCP_PORT = 5005

def multicast_send(serve:str):
    IP_server = None
    for i in range(0, 3):
        print("Try to find the server")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
        sock.sendto(serve.encode(), (MCAST_GRP, MCAST_PORT))
        sock.settimeout(uniform(3,6))
        try:
            data, addr = sock.recvfrom(50) # buffer size is 1024 bytes
            IP_server = addr[0]
            break  
        except socket.timeout:
            print("Write timeout on socket")
            continue
    return (IP_server)


def multicast_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    global stop_threads
    while not stop_threads:
        sock.settimeout(uniform(3, 6))
        try:
            data, addr = sock.recvfrom(1024)# buffer size is 1024 bytes
            print("Received message:", data.decode())
            sock.sendto(data, addr)
        except:
            continue


def TCP_process(GM):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Try to connect...")
    sock.connect((GM, TCP_PORT))
    print("Connect Successfully")
    while True:
        try:
            data = input("Enter the message: ")
            sock.send(data.encode())
            data = sock.recv(1024)
            print(data.decode())
        except KeyboardInterrupt:
            break
    print("\nClose TCP")
    sock.close()

def Manager():
    global IP_Manager
    TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_socket.bind((IP_Manager, TCP_PORT))
    try:
        TCP_socket.listen(3)

        print("ACCEPT....")
        while True:
            client_sock, client_address = TCP_socket.accept()
            print(f'Accepted connection from {client_address}')
            c_thread = threading.Thread(target=handle_client, args=(client_sock, client_address))
            c_thread.start()
    except KeyboardInterrupt:
        print('\nShutting down Server...')
        TCP_socket.close()

def handle_client(client_sock, client_address):
    """ Handle the accepted client's requests """
    try:
        data_enc = client_sock.recv(1024)
        while data_enc:
            # client's request
            name = data_enc.decode()
            resp = "hello"
            print(f'[ REQUEST from {client_address} ]')
            print('\n', name, '\n')

            # send response
            print(f'[ RESPONSE to {client_address} ]')
            client_sock.sendall(resp.encode('utf-8'))
            print('\n', resp, '\n')

            # get more data and check if client closed the connection
            data_enc = client_sock.recv(1024)
        print(f'Connection closed by {client_address}')
    except OSError as err:
        print(err)

    finally:
        print(f'Closing client socket for {client_address}...')
        client_sock.close()
        print(f'Client socket closed for {client_address}')

def Process():
    GM = multicast_send('1')
    if(GM == None):
        print("SERVER not Found")
        exit(0)
    TCP_process(GM)

def GroupManager():
    global IP_Manager
    IP_Manager = find_ip_server()
    x = threading.Thread(target=multicast_receiver)
    x.start()
    print("Start MultiCast")
    Manager()
    print("Shutting down Multicast...")
    global stop_threads
    stop_threads = True
    x.join()
    print("Shutting down")

def find_ip_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    x = s.getsockname()[0]
    s.close()
    return x


def main():
    if (len(sys.argv) != 2):
        print("Wrong Argument")
        print("0: From Group Manager")
        print("1: From Process")
        return 0
    x = int(sys.argv[1])
    if x:
        Process()
    else:
        global stop_threads
        stop_threads = False
        GroupManager()
    return 0


if __name__ == '__main__':
    main()