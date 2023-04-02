#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

import socket
from random import uniform
from _thread import *
import threading
import struct
import time
import sys
from list import *
from Group import *
from CATOC import *

MCAST_PORT = 5006
MCAST_GRP = '224.1.1.1'
MULTICAST_TTL = 2
TTL = 5
TCP_PORT = 5005
TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Stop_thread = False
msg = None
msg_r = None
view = None
list_of_processes = []


class Process:
    def __init__(self, port):
        self.UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP_sock.bind(('', port))
        self.port = port
        self.IP_Manager = None
        self.thread = None

    def multicast_send(self, message):
        for i in range(0, 3):
            print("Try to find the server")
            self.UDP_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            self.UDP_sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
            self.UDP_sock.settimeout(uniform(3, 6))
            try:
                data, addr = self.UDP_sock.recvfrom(50)  # buffer size is 1024 bytes
                self.IP_Manager = addr[0]
                break
            except socket.timeout:
                print("Write timeout on socket")
                continue

    def join_group(self, group_name, myid):
        global msg, msg_r, view
        print("I want to join the group")
        while msg != None:
            pass
        msg = "JOIN" + " " + group_name + " " + myid + " " + str(self.port)
        while msg_r == None:
            pass
        tmp = msg_r
        msg_r = None
        if tmp == "OK ":
            group_value = (11 * hash(group_name)) + (5 * hash(myid))
            while view == None:
                pass
            group = add_group(group_name, view)
            x = add_pids(group)
            view = None
            x = list_node(myid, group, group_value, x)
            list_of_processes.append(x)
            start_new_thread(UDP_send, (self.UDP_sock,))
            return (group_value)
        else:
            return -1

    def leave_group(self, value):
        global msg, msg_r, list_of_processes
        find = find_node(list_of_processes, value)
        name = find.get_group()
        id = find.get_id()
        print("I want to leave the group")
        while msg != None:
            pass
        msg = "LEAVE" + " " + name + " " + id + " " + str(self.port)
        while msg_r == None:
            pass
        tmp = msg_r
        msg_r = None
        if tmp == "OK":
            list_of_processes.remove(find)
            return True
        else:
            return False

    def TCP(self):
        global TCP_socket
        print("Try to connect...")
        TCP_socket.connect((self.IP_Manager, TCP_PORT))
        print("Connected")
        self.thread = threading.Thread(target=TCP_process)
        self.thread.start()
        print("Thread started")

    def TCP_close(self):
        global TCP_socket, Stop_thread
        Stop_thread = True
        TCP_socket.close()
        print("TCP socket closed")
        self.thread.join(timeout=1)
        print("Thread closed")

    def Group_Send(self, group_value, message, catoc):
        if catoc == 0:
            print("Sending Messages in Fifo order")
            x: list_node = find_node(list_of_processes, group_value)
            y = FIFO_RM(x.get_pids())
            message = x.get_group() + " " + message
            y.FIFO_RM_send(message)
        elif catoc == 1:
            print("Sending Messages in Catoc order")
            x: list_node = find_node(list_of_processes, group_value)
            y = CATOC_RM(x.get_pids())
            y.CATOC_RM_send(message)
        else:
            print("Is not Sending Messages in Random order")

    def Group_Receive(self, group_value, block):
        x: list_node = find_node(list_of_processes, group_value)
        if block == 0:
            return Send_to_App(0, x.get_group())
        elif block == 1:
            return Send_to_App(1, x.get_group())
        else:
            print("Is not Receiving Messages in Random order")

def TCP_process():
    global msg, msg_r, TCP_socket, Stop_thread, view, list_of_processes
    try:
        while not Stop_thread:
            if msg == None:
                try:
                    TCP_socket.settimeout(uniform(1, 3))
                    tmp = TCP_socket.recv(1024)
                    tmp = tmp.decode()
                    while view != None:
                        pass
                    if "UPDATE" in tmp:
                        print("Update received")
                        x = tmp.find("#")

                        y = add_group(tmp[6:x], tmp)
                        z = add_pids(y)
                        replace_group(list_of_processes, y, z)

                    elif "VIEW" in tmp:
                        view = tmp[4:]
                except:
                    continue
            else:
                TCP_socket.send(msg.encode())
                msg = None
                data = TCP_socket.recv(3)
                while msg_r != None:
                    pass
                msg_r = data.decode()

    except KeyboardInterrupt:
        return

def main():
    port = int(input("Enter the port number: "))
    y = Process(port)
    y.multicast_send('1')
    y.TCP()
    name, group = input("Enter the name and group of the process: ").split()
    z = y.join_group(group, name)
    try:
        if z != -1:
            while True:
                a = int(input("Press Operator to continue..."))
                if a == 1:
                    y.Group_Send(z, 'Hello', 1)
                elif a == 0:
                    y.Group_Send(z, 'Hello', 0)
                elif a < 0:
                    break
                else:
                    y.Group_Receive(z, 0)
    finally:
        y.leave_group(z)
        y.TCP_close()

if __name__ == '__main__':
    main()
        