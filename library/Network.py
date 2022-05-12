#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

import socket
from threading import Lock

mutex = Lock()
magic_char = ' '  # magic char to identify the start of the message


class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Address = (ip, port)
        self.count = 0

    def send_message(self, message, op, size):
        mutex.acquire()

        count = self.count
        self.count += 1
        message = str(count) + magic_char + message

        while True:
            self.client.sendto(message.encode(), self.Address)
            self.client.settimeout(20)  # 20 second
            try:
                if op == 'r':
                    data = self.client.recv(size).decode()
                else:
                    data = self.client.recv(1024).decode()

                if data:
                    if data[:len(str(count))] == str(count):
                        mutex.release()
                        return data[len(str(count)) + 2:]
            except:
                pass