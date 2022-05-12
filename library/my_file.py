#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from time import time_ns
#time() second
#time_ns() nanosecond

OnlyReadMode = '0'
OnlyWriteMode = '1'
TruncateMode = 512


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

    def get_data(self, size):
        """ Return a list of elements from the oldest to the newest. """
        return self.data[:size]


class File:
    def __init__(self, name, flags, server_id, size_cache, size_block, size_disk, last_modified, network):
        self.name = name
        self.flags = oct(flags)  # octal
        self.size = size_cache
        self.server_id = server_id
        self.timestamp = time_ns()
        self.size_block = size_block
        self.size_disk = size_disk
        self.last_modified = last_modified
        self.cache = RingBuffer(size_cache)
        self.file_start = 0
        self.seek = 0
        self.file_end = size_block * size_cache
        self.network = network

    def get_open(self):
        return self.open

    def get_name(self):
        return self.name

    def get_flags(self):
        return self.flags

    def get_timestamp(self):
        return self.timestamp

    def refresh_timestamp(self):
        self.timestamp = time_ns()

    def read_file(self, size):
        if self.flags[-1:] == OnlyWriteMode:
            print("Permission denied")
            return None
        if self.seek + size > self.file_end:
            message = "r " + str(self.server_id) + " " + str(self.seek) + " " + str(self.size_block * self.size_cache/3)
            resv = self.network.send_message(message, "r", size)
            if resv is None:
                return None
            self.last_modified, data = resv.split("#$")
            #TODO: REFRESH Cache
        self.seek += size
        return self.cache.get_data(size / self.size_block)

    def write_file(self, data):  # 0 to not write, len(data) to write
        if self.flags[-1:] == OnlyReadMode:
            print("Permission denied")
            return None

        message = "w " + str(self.server_id) + " " + str(self.seek) + " " + data
        rersv = self.network.send_message(message, "w", 0)
        if rersv is None:
            return None
        if "-1" in rersv:
            return None
        self.last_modified = rersv
        self.timestamp = time_ns()
        self.seek += len(data)
        return len(data)

    def seek_file(self, offset, whence):
        if whence == 0:
            self.seek = offset
        elif whence == 1:
            # TODO: REFRESH FILE
            self.seek += offset
        elif whence == 2:
            # TODO: REFRESH FILE
            self.seek = self.file_end + offset
        return self.seek

    def truncate_file(self, size):
        if len(self.flags) > 5 and self.flags[-1:] == OnlyReadMode:
            print("Permission denied")
            return None

        message = "w " + str(self.server_id) + " " + str(size) + " $#trun#$"
        rersv = self.network.send_message(message, "w", 0)
        if rersv is None:
            return None
        if "-1" in rersv:
            return None
        self.last_modified = rersv
        self.timestamp = time_ns()
        self.seek = size
        return 1

    def refresh_file(self):
        self.refresh_timestamp()
        message = "n " + str(self.server_id) + " " + str(self.last_modified)
        rersv = self.network.send_message(message, "n", 0)
        if rersv is None:
            return None
        if "OK" in rersv:
            return 1
        #TODO: REFRESH FILE
        # If it is the same, do nothing