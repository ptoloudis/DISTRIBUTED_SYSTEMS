#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from library.general import *


x = input("Enter the server's IP address: ")
buffer_size = int(input("Enter the buffer size: "))
chace_size = int(input("Enter the cache size: "))
timeout = int(input("Enter the timeout: "))
x = General(x,12001,buffer_size,chace_size,timeout)

while True:
    tmp = input("Enter the command: ")
    if tmp == "exit":
        break
    if tmp == "open":
        file = input("Enter the file name, permission: ")
        z = x.mynfs_open(file[0],file[1])
    if tmp == "close":
        file = input("Enter the file name: ")
        x.mynfs_close(file)
    if tmp == "read":
        size = int(input("Enter the size: "))
        print(x.mynfs_read(z,size))
    if tmp == "write":
        str = input("Enter the string: ")
        x.mynfs_write(z,str)
    if tmp == "seek":   
        offset = int(input("Enter the offset: "))
        x.mynfs_seek(z,offset)
    if tmp == "tell":
        print(x.mynfs_tell(z))
    if tmp =="truncate":
        size = int(input("Enter the size: "))
        x.mynfs_truncate(z,size)
