#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from library.general import *


x = input("Enter the server's IP address: ")
buffer_size = 10
chace_size = 10
timeout = 300
x = General(x,12001,buffer_size,chace_size,timeout)

z1 = x.mynfs_open("test.c", O_RDWR)
z2 = x.mynfs_open("test1.txt", O_RDONLY)

x.mynfs_read(z1,10)
input("Press Enter to continue...")
x.mynfs_read(z2,10)
input("Press Enter to continue...")
x.mynfs_read(z1,10)
input("Press Enter to continue...")
x.mynfs_read(z2,10)
input("Press Enter to continue...")
x.mynfs_write(z1,"Hello World!")
input("Press Enter to continue...")
x.mynfs_seek(z1,0)
input("Press Enter to continue...")
x.mynfs_read(z1,10)
input("Press Enter to continue...")
x.mynfs_read(z2,10)
input("Press Enter to continue...")
x.mynfs_seek(z2,50)
input("Press Enter to continue...")
x.mynfs_write(z2,10)
input("Press Enter to continue...")



