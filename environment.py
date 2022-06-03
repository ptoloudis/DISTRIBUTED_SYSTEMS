#!/usr/bin/env python3

from network import Network
import parser
import multiprocessing
from threading import Thread

buffer = multiprocessing.Manager().list()
merger = multiprocessing.Manager().list()
group = 0

list = parser.mylist

net = Network(buffer, merger, list)

Address = net.get_Address()
s = net.get_socket()

print("\033[35m Address: " + Address[0] +":"+ Address[1].__str__() + "\033[0m")
print("\033[35m press help form manual \033[35m")

rcv = multiprocessing.Process(target=net.rcv)
rcv.start()
# send = multiprocessing.Process(target=net.send())
# send.start()

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


        print("\033[35m Migrating " + thread + " to " + ip_send + ":" + port_send.__str__() + "\033[0m\n")

        s.connect((ip_send, port_send))
        try:
            s.send("migrate".encode())
            s.send((merger[0] + " " + merger[1] + " " + merger[2].__str__()) + " " + len(tmpA) + " " + len(tmpL))
            s.send(tmpA)
            s.send(tmpL)

            f = open(merger[1], "r")
            while True:
                x = f.read(2048)
                if x == "":
                    s.send("End")
                    break
                s.send(x)
            x = s.recv(2048)
            if x == b"OK":
                print("\033[35m Process " + thread + " migrated\033[0m\n")
            else:
                print("\033[35m Process " + thread + " not migrated\033[0m\n")
            merger = []
            parser.mylist.refresh()
        finally:
            s.close()

    elif operation == "exit":
        print("\033[35m The system closes.\033[0m\n")
        exit(0)

    elif operation == "shutdown":
        print("\033[35m The system shuts down.\033[0m\n")
        exit(0)

    else:
        print("\033[35m Unknown command.\033[0m\n")

    input("\033[35m Press Enter to continue...\033[0m\n")

rcv.kill()
send.kill()
             