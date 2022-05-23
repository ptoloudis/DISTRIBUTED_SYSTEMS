# File parser for SIMPLESCRIPT language

from time import sleep
from var import *
import re
from time import sleep




def parse(file, id, args, arg):
    varArray = []
    LabelArray = []
    for i in range(args):
        varArray.append(arg[i])

    file = open(file, "r")

    if file.readline().strip() != "#SIMPLESCRIPT":
        print("Invalid file")
        file.close()
        exit(1)

    while True:
        print(varArray)
        position = file.tell()
        line = file.readline()
        if line == "" :
            print("File Finished")
            break
        line = line.strip()
        if line == "":
            continue
        if line == "RET":
            print("RET")
            break
        line = re.sub("\s+", " ", line)
        if line[0] == "#":
            label,line = line.split("",1)
            current = LabelArray_find(label)
            if current == None:
                LabelArray.append(Label(label, position))
            else:
                if current.position != position:
                    print("Label already exists")
                    file.close()
                    exit(1)
        operation, line = line.split(" ", 1)
        if operation == "SET":
            var, value = line.split(" ", 1)
            print("SET", var, value)
            if len(varArray) == 0:
                if value[0] == "\"":
                    var = variables(var, "STRING", value)
                else:
                    var = variables(var, "INTEGER", value)

                varArray.append(var)
                continue
            var = varArray_find(var, varArray)
            if var == None:
                if value[0] == "\"":
                    var = variables(var, "STRING", value)
                else:
                    var = variables(var, "INTEGER", value)

                varArray.append(var)
            else:
                if value[0] == "\"" and var.type == "STRING":
                    
                    var.value = value
                elif value[0] != "\"" and var.type == "INTEGER":
                    var.value = value
                else:
                    print("ERROR : Different type of values\n")
                    file.close()
                    exit(1)

        elif operation == "ADD":
            var, value, value2 = line.split(" ", 2)
            if var[0] == "$":
                print(var)
                Val = varArray_find(var, varArray)
                if Val == None:
                    print("Variable: "+var+" does not exist\n")
                    file.close()
                    exit(1)
                elif Val.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                print("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = int(Value.value) 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value 
            else:
                tmp2 = int(value2)
            
            Val.value = tmp + tmp2

        
        elif operation == "SUB":
            var, value, value2 = line.split(" ", 2)
            if var[0] == "$":
                Val = varArray_find(var, varArray)
                if Val == None:
                    print("Variable: "+var+" does not exist\n")
                    file.close()
                    exit(1)
                elif Val.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                print("ERROR : Not valid type of variable\n")
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
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
                if Val == None:
                    print("Variable: "+var+" does not exist\n")
                    file.close()
                    exit(1)
                elif Val.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                print("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
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
                if Val == None:
                    print("Variable: "+var+" does not exist\n")
                    file.close()
                    exit(1)
                elif Val.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                print("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
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
                if Val == None:
                    print("Variable: "+var+" does not exist\n")
                    file.close()
                    exit(1)
                elif Val.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
            else:
                print("ERROR : Not valid type of variable\n")
                file.close()
                exit(1)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
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
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value 
            else:
                tmp2 = int(value2)
            
            if tmp > tmp2:
                Label1 = LabelArray_find(label)
                if Label1 == None:
                    print("Label: "+label+" does not exist\n")
                    file.close()
                    exit(1)
                else:
                    file.seek(Label1.position, 0)


        elif operation == "BGE":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value 
            else:
                tmp2 = int(value2)
            
            if tmp >= tmp2:
                Label1 = LabelArray_find(label)
                if Label1 == None:
                    print("Label: "+label+" does not exist\n")
                    file.close()
                    exit(1)
                else:
                    file.seek(Label1.position, 0)



        elif operation == "BLT":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2, varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value 
            else:
                tmp2 = int(value2)
            
            if tmp < tmp2:
                Label1 = LabelArray_find(label)
                if Label1 == None:
                    print("Label: "+label+" does not exist\n")
                    file.close()
                    exit(1)
                else:
                    file.seek(Label1.position, 0)

        
        elif operation == "BLE":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2,varArray)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value 
            else:
                tmp2 = int(value2)
            
            if tmp <= tmp2:
                Label1 = LabelArray_find(label)
                if Label1 == None:
                    print("Label: "+label+" does not exist\n")
                    file.close()
                    exit(1)
                else:
                    file.seek(Label1.position, 0)


        elif operation == "BEQ":
            value, value2, label = line.split(" ", 2)
            if value[0] == "$":
                Value = varArray_find(value, varArray)
                if Value == None:
                    print("Variable: "+value+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp = Value.value 
            else:
                tmp = int(value)
                    
            if value2[0] == "$":
                Value2 = varArray_find(value2)
                if Value2 == None:
                    print("Variable: "+value2+" does not exist\n")
                    file.close()
                    exit(1)
                elif Value2.type != "INTEGER":
                    print("ERROR : Cannot add string values\n")
                    file.close()
                    exit(1)
                else:
                    tmp2 = Value2.value 
            else:
                tmp2 = int(value2)
            
            if tmp == tmp2:
                Label1 = LabelArray_find(label)
                if Label1 == None:
                    print("Label: "+label+" does not exist\n")
                    file.close()
                    exit(1)
                else:
                    file.seek(Label1.position, 0)


        elif operation == "BRA":
            label = line
            Label1 = LabelArray_find(label)
            if Label1 == None:
                print("Label: "+label+" does not exist\n")
                file.close()
                exit(1)
            else:
                file.seek(Label1.position, 0)

        elif operation == "SLP":
            var = line
            if var[0] == "$" or var[0] =="\"":
                print("Not int in SLP\n")
                file.close()
                exit(1)
            sleep(int(var))

        elif operation == "PRN":
            var = line
            if var[0] != "$":
                print("NOT is var\n")
                file.close()
                exit(1)
            x = varArray_find(var, varArray)
            if x != None:
                print("#",id,": ",x.value)
            else:
                print("Not find "+var)

    file.close()
        


parse("input.txt",0,0,None)