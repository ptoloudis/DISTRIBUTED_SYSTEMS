from library.message import *
class buffer_send:
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
        self.cur = 0

    def add(self, message: messages):
        while(self.cur >= self.max):
            pass
        self.data.append(message)
        self.cur += 1
    
    def get(self):
        if(self.cur <= 0):
            return None
        else:
            self.cur -= 1
            return self.data.pop(0)

class buffer_re:
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
        self.cur = 0

    def add(self, message: messages):
        while(self.cur >= self.max):
            pass
        self.data.append(message)
        self.cur += 1
    
    def get(self, id):
        i = 0
        while True:
            while(i in range(self.cur)):
                if(self.data[i].id == id):
                    self.cur -= 1
                    return self.data[i]

    def find(self, mes: str):
        for i in range(self.cur):
            if(self.data[i].message == str):
                return 0
        return 1
