# File parser for SIMPLESCRIPT language

from __future__ import print_function
from threading import Lock
from multiprocessing import Process
from var import *
from time import sleep

import re
import sys

mutex = Lock()

class myList:
    def __init__(self):
        self.list = []
    def input(self, id, name, args, pros):
        for i in self.list:
            z = i.get_pros()
            if not z.is_alive():
                self.list.remove(i)
        tmp = process(id, name, args, pros)
        self.list.append(tmp)

    def __str__(self):
        for i in self.list:
            z = i.get_pros()
            if not z.is_alive():
                self.list.remove(i)
        for i in self.list:
            print(i.__str__())

    def get_pros(self, id):
        for i in self.list:
            if i.id == id:
                return i.get_pros()

    def __del__(self):
        self.list = []


mylist = myList()


class process:
    def __init__(self, id, program_name, args, pros: Process):
        self.id = id
        self.program_name = program_name  
        self.args = args 
        self.pros: Process = pros
    def __str__(self):
        return str(self.id) + " " + self.program_name + " " + self.args 

    def get_pros(self):
        return self.pros


def eprint(*args, **kwargs):
    sys.stdout.flush()
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()

def parse(file_name, id, arg):
    varArray = []
    LabelArray = []


    varArray.append(variables("$arg0", "STRING", file_name))

    args = 0
    while arg != "":
        tmp = "$arg" + str(args+1)
        try:
            temp, arg = arg.split(" ", 1)
        except:
            temp = arg
            arg = ""
        if temp[0] == "\"":
            varArray.append(variables(tmp, "STRING", temp))
        else:
            varArray.append(variables(tmp, "INTEGER", int(temp)))
        args += 1

    varArray.append(variables("$args", "INTEGER", args + 1 ))

    try:
        file = open(file_name, "r")
    except:
        eprint("File not found")
        return

    Fd_label: Find_label = Find_label(file, 0)

    if file.readline().strip() != "#SIMPLESCRIPT":
        eprint("Invalid file")
        file.close()
        exit(1)

    while True:
        position = file.tell()
        line = file.readline()

        if line == "":
            print("File Finished")
            break
        line = line.strip()

        if line == "":
            continue

        if line == "RET":
            print("RETURN")
            break
            
        line = re.sub("\s+", " ", line)

        if line[0] == "#":
            label, line = line.split(" ", 1)
            if LabelArray == []:
                LabelArray.append(Label(label, position))
            else:
                current = LabelArray_find(label, LabelArray)
                if current is None:
                    LabelArray.append(Label(label, position))
                else:
                    if current.position != position:
                        eprint("Label "+label+" already exists")
                        file.close()
                        exit(1)
        try:
            operation, line = line.split(" ", 1)
        except:
            operation = line
            line = ""

        if operation == "SET":
            var, value = line.split(" ", 1)
            if len(varArray) == 0:
                if value[0] == "\"":
                    var = variables(var, "STRING", value)
                else:
                    var = variables(var, "INTEGER", int(value))

                varArray.append(var)
                continue
            Var = varArray_find(var, varArray)
            if Var is None:
                if value[0] == "\"":
                    var = variables(var, "STRING", value)
                else:
                    var = variables(var, "INTEGER", int(value))

                varArray.append(var)
            else:
                if value[0] == "\"" and var.type == "STRING":

                    var.value = value
                elif value[0] != "\"" and var.type == "INTEGER":
                    var.value = int(value)
                else:
                    eprint("ERROR : Different type of values\n")
                    file.close()
                    exit(1)

        elif operation == "ADD":
            var, value, value2 = line.split(" ", 2)
            if var[0] == "$":
                Val = varArray_find(var, varArray)
                if Val is None:
                    Val = variables(var, "INTEGER", 0)
                    varArray.append(Val)
                elif Val.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = int(Value.value)
            else:
                tmp = value

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = value2

            Val.value = tmp + tmp2


        elif operation == "SUB":
            var, value, value2 = line.split(" ", 2)
            if var[0] == "$":
                Val = varArray_find(var, varArray)
                if Val is None:
                    Val = variables(var, "INTEGER", 0)
                    varArray.append(Val)
                elif Val.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR : Not valid type of variable\n")
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            Val.value = tmp - tmp2


        elif operation == "MUL":
            var, value, value2 = line.split(" ", 2)
            if var[0] == "$":
                Val = varArray_find(var, varArray)
                if Val is None:
                    Val = variables(var, "INTEGER", 0)
                    varArray.append(Val)
                elif Val.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            Val.value = tmp * tmp2


        elif operation == "DIV":
            var, value, value2 = line.split(" ", 2)
            if var[0] == "$":
                Val = varArray_find(var, varArray)
                if Val is None:
                    Val = variables(var, "INTEGER", 0)
                    varArray.append(Val)
                elif Val.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            Val.value = tmp / tmp2


        elif operation == "MOD":
            var, value, value2 = line.split(" ", 2)
            if var[0] == "$":
                Val = varArray_find(var, varArray)
                if Val is None:
                    Val = variables(var, "INTEGER", 0)
                    varArray.append(Val)
                elif Val.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            Val.value = tmp % tmp2

        elif operation == "BGT":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp > tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                else:
                    if position == Label1.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)


        elif operation == "BGE":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp >= tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                else:
                    if position == Label1.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)


        elif operation == "BLT":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp < tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                else:
                    if position == Label1.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)

        elif operation == "BLE":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp <= tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                else:
                    if position == Label1.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)


        elif operation == "BEQ":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2)
                if Value2 is None:
                    eprint("Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp == tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                else:
                    if position == Label1.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)


        elif operation == "BRA":
            label = line
            Label1 = LabelArray_find(label, LabelArray)
            if Label1 is None:
                Fd_label.set_position(position)
                result, LabelArray = Fd_label.run(label, LabelArray)
                if result is None:
                    eprint("Label: " + label + " does not exist\n")
                    file.close()
                    exit(1)
                else:
                    if position == result.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(result.position, 0)
            else:
                if position == Label1.position:
                    eprint("ERROR : Infinite loop\n")
                    file.close()
                    exit(1)
                file.seek(Label1.position, 0)

        elif operation == "SND":
            label = line
            Label1 = LabelArray_find(label, LabelArray)
            if Label1 is None:
                Fd_label.set_position(position)
                result, LabelArray = Fd_label.run(label, LabelArray)
                if result is None:
                    eprint("Label: " + label + " does not exist\n")
                    file.close()
                    exit(1)
                else:
                    if position == result.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(result.position, 0)
            else:
                if position == Label1.position:
                    eprint("ERROR : Infinite loop\n")
                    file.close()
                    exit(1)
                file.seek(Label1.position, 0)

        elif operation == "RCV":
            label = line
            Label1 = LabelArray_find(label, LabelArray)
            if Label1 is None:
                Fd_label.set_position(position)
                result, LabelArray = Fd_label.run(label, LabelArray)
                if result is None:
                    eprint("Label: " + label + " does not exist\n")
                    file.close()
                    exit(1)
                else:
                    if position == result.position:
                        eprint("ERROR : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(result.position, 0)
            else:
                if position == Label1.position:
                    eprint("ERROR : Infinite loop\n")
                    file.close()
                    exit(1)
                file.seek(Label1.position, 0)

        elif operation == "SLP":
            var = line
            if var[0] == "$" or var[0] == "\"":
                eprint("Not int in SLP\n")
                file.close()
                exit(1)
            sleep(int(var))


        elif operation == "PRN":
            mutex.acquire()
            print("#", id, ": ", end="")
            while line != "":
                try:
                    var, line = line.split(" ", 1)
                except:
                    var = line
                    line = ""
                if var[0] != "$":
                    print(var, end=" ")
                else:
                    x = varArray_find(var, varArray)
                    if x is not None:
                        print(x.value, end=" ")
                    else:
                        eprint("Not find " + var)
            print()
            sys.stdout.flush()
            mutex.release()


#parse("input.txt", 0, 0, None)