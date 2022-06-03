from re import sub
from time import sleep
class variables:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    def __str__(self):
        return self.name + " " + self.type + " " + self.value.__str__()

    def get_name(self):
        return self.name
    
def varArray_find(name, varArray):
    for i in range(len(varArray)):
        if varArray[i].name == name:
            return varArray[i]
    return None


class Label:
    def __init__(self, name, position, line):
        self.name = name
        self.position = position
        self.line = line

    def __str__(self):
        return self.name + " " + self.position.__str__() + " " + self.line.__str__()

def LabelArray_find(name, LabelArray):
    for i in range(len(LabelArray)):
        if LabelArray[i].name == name:
            return LabelArray[i]
    return None

class Find_label:
    def __init__(self, file, position):
        self.file = file
        self.position = position
        self.line_pos = 0
        self.finshed = False

    def set_position(self, position, line_pos):
        if position > self.position:
            self.position = position
            self.line_pos = line_pos

    def run(self, name, LabelArray):
        if self.finshed:
            return None, LabelArray

        file = self.file
        file.seek(self.position)
        while True:
            self.line_pos += 1
            position = file.tell()
            line = file.readline()
            if line == "":
                self.finshed = True
                break
            line = line.strip()
            if line == "":
                continue
            if line == "RET":
                self.finshed = True
                break
            line = sub("\s+", " ", line)
            if line[0] == "#":
                label, line = line.split(" ", 1)
                current = LabelArray_find(label, LabelArray)
                if current == None:
                    LabelArray.append(Label(label, position, self.line_pos))
                    if label == name:
                        break
                else:
                    if current.position != position:
                        print("Label "+label +" already exists")
                        file.close()
                        exit(1)
        self.position = file.tell()
        return LabelArray_find(name, LabelArray), LabelArray


pos = 0


class Buffer:
    def __init__(self, id1, id2, *msg):
        global pos
        self.id1 = id1
        self.id2 = id2
        self.msg = msg
        self.finished = False
        pos += 1
        self.position = pos
    
    def get_position(self):
        return self.position 
    def get_finished(self):
        return self.finished
    def set_finished(self):
        print("set finished")
        self.finished = True

def BufferArray_find_pos(pos, BufferArray):
    for i in range(len(BufferArray)):
        if BufferArray[i].position == pos:
            return False
    return True

def BufferArray_find(id1, id2, *data, BufferArray):
    while True:
        for i in range(len(BufferArray)):
            k = 0
            if BufferArray[i].id1 == id1 and BufferArray[i].id2 == id2:
                for j in range(len(BufferArray[i].msg)):
                    if BufferArray[i].msg[j] == data[j] or data[j][0] == None:
                        k += 1
                        if k == len(BufferArray[i].msg):
                            msg = BufferArray[i].msg
                            BufferArray.pop(i)
                            return msg
        sleep(2)
