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
#IP_Manager = None
MULTICAST_TTL = 2
TTL = 5
TCP_PORT = 5005

class Process:
    def __init__(self):
        self.UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.TCP_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP_Manager = None
        self.counter = 0

    def multicast_send(self, message):
        for i in range(0, 3):
            print("Try to find the server")
            self.UDP_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
            self.UDP_sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
            self.UDP_sock.settimeout(uniform(3,6))
            try:
                data, addr = self.UDP_sock.recvfrom(50) # buffer size is 1024 bytes
                self.IP_Manager = addr[0]
                break  
            except socket.timeout:
                print("Write timeout on socket")
                continue
        
    def join_group(self, group_name, myid):
        print("I want to join the group")
        message = "JOIN" + " " + group_name + " " + myid
        if self.TCP_process(message):
            group_value = (11 * int(group_name)) + (5 * int(myid))
            print(group_value)
            return (group_value)
        else :
            return -1

    def leave_group(self, group_name, myid):
        print("I want to leave the group")
        message = "LEAVE" + " " + group_name + " " + myid
        if self.TCP_process(message):
            return True
        else :
            return False

    def TCP(self):
        print("Try to connect...")
        self.TCP_sock.connect((self.IP_Manager, TCP_PORT))
        print("Connect Successfully")

    def TCP_process(self, GM: str):
        try:
            # data = input("Enter the message: ")
            self.TCP_sock.send(GM.encode())
            data = self.TCP_sock.recv(1024)
            print("Received message:", data.decode())
            if "OK" in data.decode():
                return True
            else:
                return False
        except KeyboardInterrupt:
            return False


    


class Group_Info:
    def __init__(self, group_name):
        self.group_name = group_name
        self.members: Process = []

