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
    def return_message(self):
        return self.message
    def return_destination(self):
        return self.destination
    def return_checksum(self):
        return self.checksum
    def return_message_length(self):
        return self.message_length