#!/usr/bin/env python3

import parser
import multiprocessing

buffer = multiprocessing.Manager().list()
group = 0
print("\033[35m press help form manual \033[0m")

while 1:
    input1 = input("\033[35m Enter the command: \033[0m")
    if input1 == "help":
        ms = " Run the program: run <filename> <argv>\n View the running program: list\n Kill a program: kill<id>\n View the help: help\n Exit: exit\n Shutdown: shutdown\n"
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
            tmp = group.__str__() + "." + id.__str__()
            id += 1
            
            pros = multiprocessing.Process(target=parser.parse, args=(fileName, tmp, args, [], [], buffer))
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
            kill = input1 + "." + i.__str__()
            x = parser.mylist.get_pros(kill)
            if x == None:
                break
            else:
                x.terminate()
                x.join()
                print("\033[35mProcess " + kill + " killed\033[0m\n")
            i += 1
    
    elif operation == "exit":
        print("\033[35mThe system closes.\033[0m\n")
        exit(0)
    elif operation == "shutdown":
        print("\033[35mThe system shuts down.\033[0m\n")
        exit(0)

    input("\033[35mPress Enter to continue...\033[0m\n")