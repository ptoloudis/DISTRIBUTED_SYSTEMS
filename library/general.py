#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from library.my_file import *
from library.Network import Network
from sys import stderr

def perror(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


O_CREAT = 64
O_EXCL = 128
O_TRUNC = 512
O_RDWR = 2
O_RDONLY = 0
O_WRONLY = 1

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

        message = "o " + path + " " + str(flags)
        resv = self.network.send_message(message, "o", 0)
        if "File Not Created" not in resv:
            id, last_mod, size = resv.split("#")

            x: File = File(path, flags, id, self.cacheblocks, self.blocksize, int(size), int(last_mod), self.network)
            self.counter += 1
            self.files.append(Files(x, self.counter))
            print("hahahahaha")
            return self.counter
        else:
            return 0

    def mynfs_read(self, fd, size):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            if time_ns() - z.get_time > self.freshTime:
                z.refresh_file()
            x = z.read_file(size)
            if x == -1:
                self.mynfs_close(fd)
                perror("Server make a Reboot")
            return x
        else:
            return None

    def mynfs_write(self, fd, buffer):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            x = z.write_file(buffer)
            if x  == -1:
                self.mynfs_close(fd)
                perror("Server make a Reboot")
            return x

        else:
            return None

    def mynfs_seek(self, fd, offset, whence):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            if time_ns() - z.get_time > self.freshTime:
                z.refresh_file()
            x = z.seek_file(offset, whence)
            if x  == -1:
                self.mynfs_close(fd)
                perror("Server make a Reboot")
            return x

        else:
            return None


    def mynfs_truncate(self, fd, size):
        z = BinarySearch(self.files, 0, len(self.files), fd)
        if z is not None:
            x = z.truncate_file(size)
            if x  == -1:
                self.mynfs_close(fd)
                perror("Server make a Reboot")
            return x

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
