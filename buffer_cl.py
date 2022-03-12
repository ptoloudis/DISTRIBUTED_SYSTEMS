import threading


class id:
    def __init__(self ):
        self.id = 0
    def get_id(self):
        self.id += 1
        return self.id

class messeges:
    def __init___(self, destination:str, messege:bytes, messege_length:int):
        self.destination = destination
        self.messege = messege
        self.messege_length = messege_length
        self.id = id.get_id()

    def return_id(self):
        return self.id
    

class buffer_send:
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
        self.cur = 0

    def add(self, messege: messeges):
        while(self.cur >= self.max):
            pass
        self.data.append(messege)
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

    def add(self, messege: messeges):
        while(self.cur >= self.max):
            pass
        self.data.append(messege)
        self.cur += 1
    
    def get(self, id):
        i = 0
        while True:
            while(i in range(self.cur)):
                if(self.data[i].id == id):
                    self.cur -= 1
                    return self.data[i]
