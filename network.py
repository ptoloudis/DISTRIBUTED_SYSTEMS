
from os.path import exists
from random import randint
import socket
import struct
import parser
import var
import multiprocessing
import sys

remote_process = []

mylist = parser.myList()

stop  = False

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    return s.getsockname()[0]

# find a free port
def get_free_port():
    while True:
        port = randint(3000, 5000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not (sock.connect_ex(('127.0.0.1', port)) == 0):
            sock.close()
            return port

class Network:
    def __init__(self, buffer, merger):
        self.buffer = buffer
        self.merger = merger
        Address = (get_ip(), get_free_port())
        self.Address = Address
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.bind(Address)
        self.socket = mysocket
        self.i_have = None

    def get_Address(self):
        return self.Address

    def get_socket(self):
        return self.socket

    def rcv(self):
        global mylist, remote_process
        s = self.socket
        s.listen()
        buffer = self.buffer
        merger = self.merger
        while True:
            if stop:
                break
            machine, addr = s.accept()
            tmp = machine.recv(2048)

            if tmp == b"migrate":

                tmp = machine.recv(2048).decode()
                thread_id, fileName, size, position, size_var, size_label = tmp.split(" ")
                size = int(size)
                position = int(position)
                size_var = int(size_var)
                size_label = int(size_label)

                tmp = machine.recv(size_var).decode()
                varA = []
                if size_var != 0:
                    while tmp == "":
                        try:
                            name, type, value, tmp = tmp.split(" ", 3)
                        except:
                            name, type, value = tmp.split(" ", 2)
                            tmp = ""
                        if type == "INTEGER":
                            varA.append(var.Variable(name, type, int(value)))
                        elif type == "STRING":
                            varA.append(var.Variable(name, type, value))

                tmp = machine.recv(size_label).decode()
                varL = []
                pos = 0
                if size_label != 0:
                    while tmp == "":
                        try:
                            name, pos, line, tmp = tmp.split(" ", 3)
                        except:
                            name, pos, line = tmp.split(" ", 2)
                            tmp = ""
                        varL.append(var.Label(name, int(pos), int(line)))

                if exists(fileName):
                    tmp = fileName
                    while exists(tmp):
                        tmp = fileName + "_" + str(randint(0, 400))
                    fileName = tmp
                machine.send(b"migrate_ok")
                f = open(fileName, "w")
                while True:
                    x = machine.recv(2048)
                    if x.decode() == "End":
                        break
                    f.write(x.decode())
                f.close()
                pros = multiprocessing.Process(target=parser.parse, args=(fileName, thread_id, "", varA, varL, buffer, merger, position))
                pros.start()
                mylist.input(thread_id, fileName, "", pros)
                print(mylist.__str__())

            elif tmp == b"message_pros_send":
                tmp = machine.recv(2048).decode()
                thread_id1, thread_id2, message = tmp.split(" ", 2)
                z = var.Buffer(thread_id1, thread_id2, message)
                self.buffer.append(z)
                pos = z.get_position()
                remote_process.append([pos, addr, thread_id1, thread_id2, message])

            elif tmp == b"message_pros_recv":
                tmp = machine.recv(2048).decode()
                thread_id1, thread_id2, message = tmp.split(" ", 2)
                var.BufferArray_find(thread_id1, thread_id2, message, BufferArray=self.buffer)

            elif tmp == b"I_have":
                self.i_have = addr


    def send(self, list):
        global remote_process
        while True:
            for i in range(len(self.buffer)):
                id1 = self.buffer[i].get_id1()
                id2 = self.buffer[i].get_id2()
                pos = self.buffer[i].get_position()
                if list.get_pos(id1) == None:
                    self.i_have = None
                    multicast_send(id1, Address=self.Address)
                    while self.i_have == None:
                        pass
                    addr = self.i_have
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect(addr)
                    client.socket.sendall(b"message_pros_send")
                    client.socket.sendall(self.buffer[i].get_message().encode())
                    client.ocket.close()

                elif list.get_pos(id2) == None:
                    self.i_have = None
                    multicast_send(id2, Address=self.Address)
                    while self.i_have == None:
                        pass
                    addr = self.i_have
                    self.socket.connect(addr)
                    self.socket.sendall(b"message_pros_send")
                    self.socket.sendall(self.buffer[i].get_message().encode())
                    self.socket.close()

                elif var.BufferArray_find_pos(pos, self.buffer):
                    for j in range(len(remote_process)):
                        if remote_process[j][0] == pos:
                            addr = remote_process[j][1]
                            self.socket.connect(addr)
                            self.socket.sendall(b"message_pros_recv")
                            x = remote_process[j][2] + " " + remote_process[j][3]
                            self.socket.sendall(x.encode())
                            self.socket.close()
                            remote_process.pop(j)

def multicast_send(self, message, Address):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
    message = message + " " + str(Address[0]) + " " + str(Address[1])
    s.sendto(message.encode())


def multicast_rcv(list, s):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('239.192.1.100', 50000))
    mreq = struct.pack("=4sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        tmp = sock.recv(2048)
        tmp, addr, port = tmp.decode().split(" ")
        if list.get_pos(tmp.decode()) != None:
            s.connect((addr, int(port)))
            s.sendall(b"I_have")
            s.close()



