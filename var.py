from re import sub
class variables:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
    def get_name(self):
        return self.name
    
def varArray_find(name, varArray):
    for i in range(len(varArray)):
        if varArray[i].name == name:
            return varArray[i]
    return None


class Label:
    def __init__(self, name, position):
        self.name = name
        self.position = position

def LabelArray_find(name, LabelArray):
    for i in range(len(LabelArray)):
        if LabelArray[i].name == name:
            return LabelArray[i]
    return None

class Find_label:
    def __init__(self, file, position):
        self.file = file
        self.position = position
        self.finshed = False

    def set_position(self, position):
        if position > self.position:
            self.position = position

    def run(self, name, LabelArray):
        if self.finshed:
            return None, LabelArray

        file = self.file
        file.seek(self.position)
        while True:
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
                    LabelArray.append(Label(label, position))
                    if label == name:
                        break
                else:
                    if current.position != position:
                        print("Label "+label +" already exists")
                        file.close()
                        exit(1)
        self.position = file.tell()
        return LabelArray_find(name, LabelArray), LabelArray


