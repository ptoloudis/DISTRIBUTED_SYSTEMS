import threading


class serveries:
    def __init__(self):
        self.id[3][3] = []
        self.index = 0
    def add_id(self, id,ip):
        self.id[self.index][0] = id
        self.id[self.index][1] = ip
        self.id[self.index][2] = 10
        self.index += 1
    def get_id(self,id):
        for i in range(0,self.index):
            if self.id[i][0] == id and self.id[i][2] > 0:
                return self.id[i][1]
        return 0;
    def down_id(self,id):
        for i in range(0,self.index):
            if self.id[i][0] == id:
                self.id[i][2] -= 1
                return
        return;

        

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
