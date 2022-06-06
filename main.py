#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from library.general import *


x = General('172.18.61.92', 12001, 10, 10, 5)


# x, z= input('Enter the file name: ')
z = x.mynfs_open("small.txt", O_RDWR)   

print(x.mynfs_truncate(z,10))
# print(x.mynfs_write(z, 20))
# print(x.mynfs_read(z, 10))
# print(x.mynfs_read(z, 10))
# /mnt/d/github/DISTRIBUTED_SYSTEMS
