#!/usr/bin/env python3
import socket
from random import randint
import var
import parser
import multiprocessing

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


buffer = multiprocessing.Manager().list()
merger = multiprocessing.Manager().list()
group = 0

Address = (get_ip(), get_free_port())
print("\033[35m Address: " + Address[0] + ":" + str(Address[1]) + "\033[0m")
print("\033[35m press help form manual \033[35m")

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
        print("\033[35m" + merger[0] + "\033[0m")
        print("\033[35m" + merger[1] + "\033[0m")
        print("\033[35m" + merger[2].__str__() + "\033[0m")
        print("\033[35m" + merger[3].__str__() + "\033[0m")
        for i in range(len(merger[4])):
            print("\033[35m" + merger[4][i].__str__() + "\033[0m")
        print("\033[35m" + merger[5].__str__() + "\033[0m")


    elif operation == "exit":
        print("\033[35m The system closes.\033[0m\n")
        exit(0)

    elif operation == "shutdown":
        print("\033[35m The system shuts down.\033[0m\n")
        exit(0)

    else:
        print("\033[35m Unknown command.\033[0m\n")

    input("\033[35m Press Enter to continue...\033[0m\n")
