from multiprocessing.sharedctypes import Value

arg = '1 3 "hello there" 5'

args = 0
while arg != "":
    tmp = "$argv" + str(args + 1)
    try:
        temp, arg = arg.split(" ", 1)
    except:
        temp = arg
        arg = ""

    if temp[0] == "\"":
        x, arg = arg.split("\"")
        temp = temp + " " + x + "\""
        arg = arg[1:]
        print(temp+"str")
    else:
        print(temp+"int")
    args += 1