from library.hash import hash

class messages:
    def __init___(self, destination, message, message_length):
        self.destination = destination
        self.message = message
        self.checksum = hash(message)
        self.message_length = message_length
        self.id = id.get_id()

    def return_id(self):
        return self.id