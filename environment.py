#!/usr/bin/env python3
import socket
from random import randint
import var
import parser
import multiprocessing
from threading import Thread

# find the my ip address
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
            return port

def migrate_rcv(s:socket.socket,list):
    s.listen()
    while True:
        machine, addr = s.accept()
        
        tmp = machine.recv(2048)
        thread_id, fileName, size, size_var, size_label = tmp.split(" ")
        size = int(size)
        size_var = int(size_var)
        size_label = int(size_label)
        tmp = machine.recv(size_var)
        varA = []
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
        
        tmp = machine.recv(size_label)
        varL = []
        while tmp == "":
            try:
                name, pos, line, tmp = tmp.split(" ", 3)
            except:
                name, pos, line = tmp.split(" ", 2)
                tmp = ""
            varL.append(var.Label(name, int(pos), int(line))) 
        
        f = open(fileName, "w")
        while True:
            x = machine.recv(2048)
            if x == b"End":
                break
            f.write(x.decode())
        f.close()
        s.sendall(b"OK")
        pros = multiprocessing.Process(target=parser.parse, args=(fileName, thread_id , 0, varA, varL, buffer, merger))
        pros.start()
        parser.mylist.input(tmp, fileName, args, pros)


# MAIN

buffer = multiprocessing.Manager().list()
merger = multiprocessing.Manager().list()
group = 0


Address = (get_ip(), get_free_port())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM).bind(Address)

print("\033[35m Address: " + Address[0] + ":" + str(Address[1]) + "\033[0m")
print("\033[35m press help form manual \033[35m")

Thread(target=migrate_rcv, args=(s,buffer)).start()

while 1:
    input1 = input("\033[35m Enter the command: \033[0m")
    if input1 == "help":
        ms = " Run the program: run <filename> <argv>\n View the running program: list\n Kill a program: kill</group> or <ip:port/group>\n Sent to another pos: migrate <grp id> <thread id> <ip addr> <port>\n View the help: help\n Exit: exit\n Shutdown: shutdown\n"
        print("\033[35m"+ms+"\033[0m")

    try:
        operation, input1 = input1.split(" ", 1)
    except:
        operation = input1
        input1 = ""
    
    if operation == "run":
        group += 1
        id = 0
        while True:
            try:
                str, input1 = input1.split(" || ", 1)
            except:
                str = input1
                input1 = ""
            try:
                fileName, args = str.split(" ", 1)
            except:
                fileName = str
                args = ""
            tmp = Address[0] + ":" + Address[1].__str__()+"/" + group.__str__() + "." + id.__str__()
            id += 1
            
            pros = multiprocessing.Process(target=parser.parse, args=(fileName, tmp, args, [], [], buffer, merger))
            pros.start()
            parser.mylist.input(tmp, fileName, args, pros)

            if input1 == "":
                break

    elif operation == "list":
        parser.mutex.acquire()
        parser.mylist.__str__()
        parser.mutex.release()

    elif operation == "kill":
        i = 0
        while True:
            if input1[0] == "/":
                input1 = Address[0] + ":" + Address[1].__str__()+ input1

            kill = input1 + "." + i.__str__()
            x = parser.mylist.get_pros(kill)
            if x == None:
                break
            else:
                x.terminate()
                x.join()
                print("\033[35m Process " + kill + " killed\033[0m\n")
            i += 1

    elif operation == "migrate":

        try:
            group_id, input1 = input1.split(" ", 1)
            thread_id, input1 = input1.split(" ", 1)
            ip_send, input1 = input1.split(" ", 1)
            port_send = int(input1)
            input1 = ""
        except:
            print("\033[35m Invalid input\033[0m\n")
            continue

        if group_id[0] == "/":
            group_id = Address[0] + ":" + Address[1].__str__() + group_id

        thread = group_id + "." + thread_id
        if parser.mylist.get_pros(thread) == None:
            print("\033[35m Process " + thread + " not found\033[0m\n")
            continue

        merger.append(thread)
        while len(merger) != 5:
            pass

        tmpA = "" 
        for i in range(len(merger[4])):
            tmpA += merger[4][i].__str__() + " "

        tmpL = ""
        for i in range(len(merger[5])):
            tmpL += merger[5][i].__str__() + " "
        

        s.connect((ip_send, port_send))
        s.sendall((merger[0] + " " + merger[1] + " " + merger[2].__str__()) + " " + len(tmpA) + " " + len(tmpL))
        s.sendall(tmpA)
        s.sendall(tmpL)       

        f = open(merger[1], "r")
        while True:
            x = f.read(2048)
            if x == "":
                s.sendall("End")
                break
            s.sendall(x)
        x = s.recv(2048)
        if x == b"OK":
            print("\033[35m Process " + thread + " migrated\033[0m\n")
        else:
            print("\033[35m Process " + thread + " not migrated\033[0m\n")
        merger = []


    elif operation == "exit":
        print("\033[35m The system closes.\033[0m\n")
        exit(0)

    elif operation == "shutdown":
        print("\033[35m The system shuts down.\033[0m\n")
        exit(0)

    else:
        print("\033[35m Unknown command.\033[0m\n")

    input("\033[35m Press Enter to continue...\033[0m\n")


             