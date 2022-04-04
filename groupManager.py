#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

import socket
from random import uniform
import threading
import struct
import sys
from time import sleep
from tokenize import group
from Process import Process
from Group import Group, Process_Info, Group_List

MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
IP_Manager = None
MULTICAST_TTL = 2
TTL = 5
TCP_PORT = 5005
stop_threads = False
update = []


def multicast_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    global stop_threads
    while not stop_threads:
        sock.settimeout(uniform(1, 3))
        try:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print("Received message:", data.decode())
            sock.sendto(data, addr)
        except:
            continue
    sock.close()

def Manager():
    global IP_Manager, stop_threads
    group_list = Group_List()
    TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_socket.bind((IP_Manager, TCP_PORT))
    try:
        TCP_socket.listen(3)

        print("ACCEPT....")
        while True:
            client_sock, client_address = TCP_socket.accept()
            print(f'Accepted connection from {client_address}')
            c_thread = threading.Thread(target=handle_client, args=(client_sock, client_address, group_list))
            c_thread.start()
    except KeyboardInterrupt:
        print('\nShutting down Server...')
        stop_threads = True
        TCP_socket.close()

def handle_client(client_sock, client_address, group_list):
    global stop_threads, update
    my_group = []
    len_update = 0
    try:
        while not stop_threads:
            client_sock.settimeout(1)
            try:
                data_enc = client_sock.recv(1024)
                data = data_enc.decode()
                if "JOIN" in data:
                    print("JOIN")
                    group_name = data.split(" ")[1]
                    id = data.split(" ")[2]
                    x = group_list.find_group(group_name)
                    member = Process_Info(id, client_address[0], client_address[1])
                    if x == None:
                        x = Group(group_name)
                        x.add_member(member)
                        group_list.add_group(x)
                        client_sock.sendall(b'OK ')
                        my_group.append(group_name)
                        tmp = "VIEW" + x.toString()
                        print("SENDING:", tmp)
                        client_sock.sendall(tmp.encode())
                    else:
                        if x.find_members(member):
                            client_sock.sendall(b'NOK')
                        else:
                            update.append(group_name)
                            len_update += 1
                            my_group.append(group_name)
                            x.add_member(member)
                            client_sock.sendall(b'OK ')
                            tmp = "VIEW" + x.toString()
                            print("SENDING:", tmp)
                            client_sock.sendall(tmp.encode())
                elif "LEAVE" in data:
                    print("LEAVE")
                    group_name = data.split(" ")[1]
                    id = data.split(" ")[2]
                    x = group_list.find_group(group_name)
                    member = Process_Info(id, client_address[0], client_address[1])
                    if x == None:
                        client_sock.sendall(b'NOK')
                    else:
                        z = x.find_members(member)
                        if z != None:
                            x.remove_member(z)
                            client_sock.sendall(b'OK')
                            update.append(group_name)
                            my_group.remove(group_name)
                        else:
                            client_sock.sendall(b'NOK')
            except:
                if len(update) > len_update:
                    for i in range(len_update, len(update)):
                        if update[i] in my_group:
                            x = group_list.find_group(update[i])
                            tmp = "UPDATE" + x.toString()
                            print("UPDATE:", tmp)
                            client_sock.sendall(tmp.encode())
                            len_update = len(update)
    except KeyboardInterrupt:
        print('\nShutting down Client...')
    except OSError as err:
        print(err)
    finally:
        print(f'Closing client socket for {client_address}...')
        client_sock.close()
        print(f'Client socket closed for {client_address}')

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
        y = Process()
        y.multicast_send('1')
        y.TCP()
        z = y.join_group('1', '5')
        if z != -1:
            try:
                input("Press Enter to continue...")
            finally:
                y.leave_group(z)
                y.TCP_close()


    else:
        global stop_threads
        stop_threads = False
        GroupManager()
    return 0

if __name__ == '__main__':
    main()
