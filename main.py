#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from library.general import *


x = General('192.168.1.65', 12001, 5, 5, 10000)


# x, z= input('Enter the file name: ')
z = x.mynfs_open("small.txt", O_WRONLY)   

print(x.mynfs_truncate(z,5))
# x.mynfs_seek(z,522,0)
# print(x.mynfs_write(z, "hi_ioanna"))
# print(x.mynfs_read(z, 20))
# print(x.mynfs_read(z, 10))
# /mnt/d/github/DISTRIBUTED_SYSTEMS/files