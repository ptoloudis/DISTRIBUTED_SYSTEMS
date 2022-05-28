#!/usr/bin/env python3

from cmath import e
from threading import Thread
import parser

from multiprocessing import Process



group = 0

while 1:
    input("Press Enter to continue...")
    input1 = input("Enter the command: ")
    if input1 == "":
        pass
        #Help
        #print("Help: run, list, kill")
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
            
            pros = Process(target= parser.parse, args=(fileName, tmp, len(args), args)).start()
            info = parser.myList(tmp, fileName, args, pros)
            parser.mylist.append(info)

            if input1 == "":
                break

    elif operation == "list":
        parser.mutex.acquire()
        print("The list of running programs:")
        for i in parser.mylist:
            print(i.__str__())
        parser.mutex.release()
    elif operation == "kill":
        for j in parser.mylist:
            if j.id == input1:
                proc = j.get_pros()
                proc.terminate()
                parser.mylist.remove(j)
                break
    elif operation == "exit":
        exit(0)