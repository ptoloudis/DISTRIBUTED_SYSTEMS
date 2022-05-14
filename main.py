#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from library.general import *


x = General('192.168.2.4', 12001, 0, 0, 5)

z = x.mynfs_open("distrsys_s22_Assignment3.pdf", O_RDONLY)
x.mynfs_read(z, 10)

# /home/sabrina/code/DISTRIBUTED_SYSTEMS/files