from library.hash import hash

class messeges:
    def __init___(self, destination, messege, messege_length):
        self.destination = destination
        self.messege = messege
        self.checksum = hash(messege)
        self.messege_length = messege_length
        self.id = id.get_id()

    def return_id(self):
        return self.id