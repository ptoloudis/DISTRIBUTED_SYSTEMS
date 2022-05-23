class variables:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
    
def varArray_find(name, varArray):
    for i in range(len(varArray)):
        if i.name == name:
            return i
    return None


class Label:
    def __init__(self, name, position):
        self.name = name
        self.position = position

def LabelArray_find(name, LabelArray):
    for i in LabelArray:
        if i.name == name:
            return i
    return None