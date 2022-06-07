#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from time import time

#time() second
#time_ns() nanosecond

OnlyReadMode = '0'
OnlyWriteMode = '1'


class RingBuffer:
    """ class that implements a not-yet-full buffer """

    def __init__(self, size_max):
        self.cur = None
        self.max = size_max
        self.data = []

    class __Full:
        """ class that implements a full buffer """

        def __init__(self):
            self.cur = None

        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur + 1) % self.max

        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:] + self.data[:self.cur]

        def get_data(self, start, size):
            """ Return a list of elements from the oldest to the newest. """
            return self.data[start:start + size]

        

    def append(self, x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data

    def get_data(self, start, size):
        """ Return a list of elements from the oldest to the newest. """
        return self.data[start:start+size]


class File:
    def __init__(self, name, flags, server_id, size_cache, size_block, size_disk, last_modified, network):
        self.name = name
        self.flags = oct(flags)  # octal
        self.size = size_cache
        self.server_id = server_id
        self.timestamp = time()
        self.size_block = size_block
        self.size_disk = size_disk
        self.my_modification = 0
        self.last_modified = last_modified
        if self.flags[-1:] != OnlyWriteMode:
            self.cache = RingBuffer(size_cache)
            self.load = False
        else:
            self.load = True
            self.cache = None

        self.file_start = 0
        self.seek = 0
        self.file_end = size_block * size_cache
        self.network = network

    def get_name(self):
        return self.name

    def get_flags(self):
        return self.flags

    def get_timestamp(self):
        return self.timestamp

    def refresh_timestamp(self):
        self.timestamp = time()

    def read_file(self, size):
        if self.flags[-1:] == OnlyWriteMode:
            print("Permission denied")
            return None

        if self.seek> self.file_end:
            return "File end"

        elif self.seek + size > self.size_disk:
            size = self.size_disk - self.seek
            message = "r " + self.server_id + " " + str(self.seek) + " " + str(size)
            resv = self.network.send_message(message, "r", 0)
            if resv == None:
                return None
            if resv == "Reboot":
                return -1
            if "-1" in resv:
                return None
            self.last_modified = resv
            self.timestamp = time()
            self.cache.append(resv)
            self.seek += size
            return resv

        if (not self.load) or (self.my_modification != 0 and self.my_modification > self.seek):
            message = "r " + self.server_id + " " + str(self.seek) + " " + str(self.size_block * self.size)
            resv = self.network.send_message(message, "r", size)
            if resv == None:
                return None
            if resv == "Reboot":
                return -1
            
            x =resv
            num_of_msg, self.last_modified, data = x.split("#")
    
            for i in range(0, self.size):
                x = self.cache.get_data(0,self.size)
                self.cache.append(data[i * self.size_block:(i + 1) * self.size_block])
            self.my_modification = 0  # reset modification counter

        elif self.seek + size > self.file_end:
            message = "r " + self.server_id + " " + str(self.seek) + " " + str(self.size_block * int(self.size/3 + 1))
            resv = self.network.send_message(message, "r", size)
            if resv == None:
                return None
            if resv == "Reboot":
                return -1
            num_of_msg, self.last_modified, data = resv.split("#")
            for i in range(0, 3):
                self.cache.get_data(0,self.size)
                self.cache.append(data[i*self.size_block:(i+1)*self.size_block])
        msg = self.cache.get_data(int(self.seek / self.size_block), int(size / self.size_block))
        self.seek += size
        self.load = True
        tmp = ""
        for i in range(0, len(msg)):
            tmp += msg[i]
        return tmp

    def write_file(self, data):  # 0 to not write, len(data) to write
        if self.flags[-1:] == OnlyReadMode:
            print("Permission denied")
            return None

        message = "w " + self.server_id + " " + str(self.seek) + " " + data.__str__()
        resv = self.network.send_message(message, "w", 0)
        if resv == None:
            return None
        if resv == "Reboot":
            return -1
        if "-1" in resv:
            return None
        self.last_modified = resv
        self.my_modification = self.seek  # set modification counter to current seek
        self.timestamp = time()
        self.seek += len(data.__str__())
        return len(data.__str__())

    def seek_file(self, offset, whence):
        if whence == 0:
            self.seek += offset
        elif whence == 1 and self.seek - (self.size_block * self.size_cache) != 0:
            self.seek = offset
            self.read_file(self.size_block * self.size_cache)
        elif whence == 1:
            self.seek = offset
        elif whence == 2 and self.seek + offset < self.file_end:
            self.seek = self.file_end - offset
            message = "r " + self.server_id + " " + str(self.file_end - offset) + " " + str(self.size_block * self.size_cache)
            self.read_file(self.size_block * self.size_cache)
        elif whence == 2:
            self.seek = self.file_end - offset
        return self.seek

    def truncate_file(self, size):
        if len(self.flags) < 5 and self.flags[-1:] == OnlyReadMode:
            print("Permission denied")
            return None

        message = "w " + self.server_id + " " + str(size) + " $#trun#$"
        resv = self.network.send_message(message, "w", 0)
        if resv == None:
            return None
        if resv == "Reboot":
            return -1
        if "-1" in resv:
            return None
        self.last_modified = resv
        self.my_modification = size  # set modification counter to current seek
        self.timestamp = time()
        self.seek = size
        return 1

    def refresh_file(self):
        self.refresh_timestamp()
        message = "n " + self.server_id + " " + str(self.last_modified)
        resv = self.network.send_message(message, "n", 0)
        if resv == None:
            return None
        if resv == "Reboot":
            return -1
        if "OK" in resv:
            return 1
        else:
            message = "r " + self.server_id + " " + str(self.seek) + " " + str(self.size_block * self.size_cache)
            resv = self.network.send_message(message, "r", self.size_block * self.size_cache)
            if resv == None:
                return None
            self.last_modified, data = resv.split("#$")
            for i in range(0, self.size_cache):
                self.cache.get_data()
                self.cache.append(data[i * self.size_block:(i + 1) * self.size_block])
            return 0
