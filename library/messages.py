from library.hash import hash
from library.id import *

class myMes:
    def __init__(self, destination, message, Id):
        self.destination = destination
        self.message = message
        self.checksum = hash(message)
        self.message_length = len(message)
        self.id = Id.get_id()
    def return_id(self):
        return self.id