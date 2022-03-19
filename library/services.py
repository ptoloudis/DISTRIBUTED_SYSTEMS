class services:
    def __init__(self):
        self.id = [[0,0,0],[0,0,0],[0,0,0]]
        self.index = 0
    def add_id(self, ids,ip,port):
        self.id[self.index][0] = ids
        self.id[self.index][1] = ip
        self.id[self.index][2] = 10
        self.index += 1
    def get_id(self,ids):
        for i in range(0,self.index):
            if self.id[i][0] == ids and self.id[i][3] > 0:
                return self.id[i][1]
        return 0
    def get_ip(self,ids):
        for i in range(0,self.index):
            if self.id[i][0] == ids:
                return self.id[i][1]
        return 0
    def down_id(self,ids):
        for i in range(0,self.index):
            if self.id[i][0] == ids:
                self.id[i][3] -= 1
                return
        return