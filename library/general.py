#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from my_file import *
from Network import Network


class Files:
    def __init__(self, file, file_id):
        self.file: File = file
        self.file_id = file_id

    def get_file(self):
        return self.file

    def get_file_id(self):
        return self.file_id


class General:
    def __init__(self, ipaddr, port, cacheblocks, blocksize, freshTime):
        self.cacheblocks = cacheblocks
        self.blocksize = blocksize
        self.freshTime = freshTime
        self.network = Network(ipaddr, port)
        self.files = []  # list of id to files
        self.counter = 0  # counter for files

    def mynfs_open(self, path, flags):

        # ToDo: check if file exists in server
        # if is ok, add to cache
        if 1:  # if file exists in server
            size = None
            last_mod = None
            x: File = File(path, flags, self.network, self.cacheblocks, self.blocksize, size, last_mod, self.network)
            x.open_file()
            self.counter += 1
            self.files.append(Files(x, self.counter))
        else:
            return 0

    def mynfs_read(self, fd, size):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            if time_ns() - z.get_time > self.freshTime:
                z.refresh_file()
            return z.read_file(size)
        else:
            return None

    def mynfs_write(self, fd, buffer):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            return z.write_file(buffer)
        else:
            return None

    def mynfs_seek(self, fd, offset, whence):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            if time_ns() - z.get_time > self.freshTime:
                z.refresh_file()
            return z.seek_file(offset, whence)
        else:
            return None


    def mynfs_truncate(self, fd, size):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            return z.truncate_file(size)
        else:
            return None


    def mynfs_close(self, fd):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
                self.files.remove(z)
                return 1
        return 0


def BinarySearch( list:Files, start, end, item):
    if start > end:
        return None
    mid = (start + end) // 2
    if list[mid].get_file_id == item:
        return list[mid]
    elif list[mid].get_file_id > item:
        return BinarySearch(list, start, mid - 1, item)
    else:
        return BinarySearch(list, mid + 1, end, item)
