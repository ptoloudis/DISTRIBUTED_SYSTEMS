# File parser for SIMPLESCRIPT language
import os
from threading import Lock
from multiprocessing import Process
from var import *
from time import sleep

import re
import sys


mtx = Lock()
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
        return None

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

def parse(file_name, id, arg, varArr, LabelArr, BufferArray, merger):
    varArray = varArr
    LabelArray = LabelArr

    varArray.append(variables("$arg0", "STRING", file_name))

    args = 0
    while arg != "":
        tmp = "$argv" + str(args+1)
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

    varArray.append(variables("$args", "INTEGER", args + 1))

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


    line_pos = 1
    while True:
        line_pos += 1
        position = file.tell()

        if len(merger) > 0:
            if merger[0] == id:
                merger.append(file_name)
                merger.append(file_size(file_name))
                merger.append(position)
                merger.append(varArray)
                merger.append(LabelArray)
                print("Merger")
                return

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
                LabelArray.append(Label(label, position, line_pos))
            else:
                current = LabelArray_find(label, LabelArray)
                if current is None:
                    LabelArray.append(Label(label, position, line_pos))
                else:
                    if current.position != position:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + ": Label "+label+" already exists")
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
                elif value[0] == "$":
                    tmp = varArray_find(value, varArray)
                    if tmp is None:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + ": Variable "+value+" not found")
                        file.close()
                        exit(1)
                    var = variables(var, tmp.type, tmp.value)
                else:
                    var = variables(var, "INTEGER", int(value))
                varArray.append(var)
            else:
                if value[0] == "\"" and var.type == "STRING":
                    var.value = value
                elif value[0] == "$":
                    tmp = varArray_find(value, varArray)
                    if tmp is None:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + ": Variable "+value+" not found")
                        file.close()
                        exit(1)
                    var = variables(var, tmp.type, tmp.value)
                elif var.type == "INTEGER":
                    var = variables(var, "INTEGER", int(value))
                else:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Different type of values\n")
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
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = int(Value.value)
            else:
                tmp = value

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
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
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Not valid type of variable\n")
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
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
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
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
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
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
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
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
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp > tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position, line_pos)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                        line = result.line - 1
                else:
                    if position == Label1.position:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                        file.close()
                        exit(1)
                    line = result.line - 1
                    file.seek(Label1.position, 0)


        elif operation == "BGE":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp >= tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position, line_pos)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                        line = result.line - 1
                else:
                    if position == Label1.position:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)
                    line = result.line - 1


        elif operation == "BLT":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp < tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position, line_pos)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                            line = result.line - 1
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                else:
                    if position == Label1.position:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)
                    line = result.line - 1


        elif operation == "BLE":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp <= tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position, line_pos)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                        line = result.line - 1
                else:
                    if position == Label1.position:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)
                    line = result.line - 1


        elif operation == "BEQ":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value
            else:
                tmp = int(value)

            if value2[0] == "$":
                Value2 = varArray_find(value2)
                if Value2 is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + value2 + " does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value
            else:
                tmp2 = int(value2)

            if tmp == tmp2:
                Label1 = LabelArray_find(label, LabelArray)
                if Label1 is None:
                    Fd_label.set_position(position, line_pos)
                    result, LabelArray = Fd_label.run(label, LabelArray)
                    if result is None:
                        eprint("Label: " + label + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        if position == result.position:
                            eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                            file.close()
                            exit(1)
                        file.seek(result.position, 0)
                        line = result.line - 1
                else:
                    if position == Label1.position:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(Label1.position, 0)
                    line = result.line - 1


        elif operation == "BRA":
            label = line
            Label1 = LabelArray_find(label, LabelArray)
            if Label1 is None:
                Fd_label.set_position(position, line_pos)
                result, LabelArray = Fd_label.run(label, LabelArray)
                if result is None:
                    eprint("Label: " + label + " does not exist\n")
                    file.close()
                    exit(1)
                else:
                    if position == result.position:
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                        file.close()
                        exit(1)
                    file.seek(result.position, 0)
                    line = result.line - 1
            else:
                if position == Label1.position:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Infinite loop\n")
                    file.close()
                    exit(1)
                file.seek(Label1.position, 0)
                line = Label1.line - 1


        elif operation == "SND":
            data = []
            id2, value = line.split(" ", 1)
            if id2[0] == "$":
                Value = varArray_find(id2, varArray)
                if Value is None:
                    eprint("Variable: " + id2 + " does not exist\n")
                    file.close()
                    exit(1)
                else:
                    tmp, tmp2 = id.split("/", 1)
                    tmp = tmp + "/" + tmp2.split(".")[0] + "." + Value.value.__str__()
            if not isGroup(id, id2):
                eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot send to different group\n")
                file.close()
                exit(1)

            while True:
                if value == "":
                    break
                try:
                    tmp_data, value = value.split(" ", 1)
                except:
                    tmp_data = value
                    value = ""
                if tmp_data[0] == "$":
                    Value = varArray_find(tmp_data, varArray)
                    if Value is None:
                        eprint("Variable: " + tmp_data + " does not exist\n")
                        file.close()
                        exit(1)
                    else:
                        tmp_data = Value.value
                data.append(tmp_data)
            mtx.acquire()
            z = Buffer(id, id2, tuple(data))
            BufferArray.append(z)
            pos = z.get_position()
            mtx.release()
            while BufferArray_find_pos(pos, BufferArray) is False:
                sleep(1)
            mtx.acquire()
            mtx.release()


        elif operation == "RCV":
            var = []
            data = []
            id1, value = line.split(" ", 1)
            if id1[0] == "$":
                Value = varArray_find(id1, varArray)
                if Value is None:
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + id1 + " does not exist\n")
                    file.close()
                    exit(1)
                else:
                    tmp, tmp2 = id.split("/", 1)
                    tmp = tmp + "/" + tmp2.split(".")[0] + "." + Value.value.__str__()
                if not isGroup(id, id2):
                    eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot send to different group\n")
                    file.close()
                    exit(1)

            if not isGroup(id, id1):
                eprint("ERROR id " + id + " line " + line_pos.__str__() + " : Cannot send to different group\n")
                file.close()
                exit(1)

            while True:
                if value == "":
                    break
                try:
                    tmp_data, value = value.split(" ", 1)
                except:
                    tmp_data = value
                    value = ""
                if tmp_data[0] == "$":
                    Value = varArray_find(tmp_data, varArray)
                    if Value is None:
                        var.append(tmp_data)
                        tmp_data = None
                    else:
                        tmp_data = Value.value
                data.append(tmp_data)
            data = tuple(data)
            id2 = id
            data2 = BufferArray_find(id1, id2, data, BufferArray=BufferArray)
            data2 = list(data2[0])
            for i in range(len(data2)):
                if data[i] is None:
                    if data2[i] == "\"":
                        varx = variables(var[i], "STRING", data2[i])
                    else:
                        varx = variables(var[i], "INTEGER", int(data2[i]))
                    varArray.append(varx)
            var.clear()


        elif operation == "SLP":
            var = line
            if var[0] == "$" or var[0] == "\"":
                eprint("ERROR id " + id + " line " + line_pos.__str__() + ": Not int in SLP\n")
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
                        eprint("ERROR id " + id + " line " + line_pos.__str__() + " Variable: " + var + " does not exist\n")
                        file.close()
                        exit(1)
            print()
            sys.stdout.flush()
            mutex.release()



def file_size(file):
    size = os.stat(file)
    return size.st_size

def isGroup(id1, id2):
    if id1.split(".")[:3] == id2.split(".")[:3]:
       return True
    else:
        return False
