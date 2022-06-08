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

z1 = x.mynfs_open("small.txt", O_RDWR)
z2 = x.mynfs_open("medium.txt", O_RDONLY)

print("Open small.txt")
x.mynfs_read(z1,10)
input("Press Enter to continue...")
print("Open medium.txt")
x.mynfs_read(z2,10)
input("Press Enter to continue...")
print("Read 10 bytes from small.txt")
print(x.mynfs_read(z1,10))
input("Press Enter to continue...")
print("Read 10 bytes from medium.txt")
print(x.mynfs_read(z2,10))
input("Press Enter to continue...")
print("Write \"Hi from test1!\" from small.txt")
x.mynfs_write(z1,"Hi from test1!")
input("Press Enter to continue...")
print("seek to the beginning of small.txt")
x.mynfs_seek(z1,0)
print("Read 10 bytes from small.txt")
print(x.mynfs_read(z1,10))
input("Press Enter to continue...")
print("Read 10 bytes from medium.txt")
print(x.mynfs_read(z2,10))
input("Press Enter to continue...")
print("Seek to the 50th byte of medium.txt")
x.mynfs_seek(z2,50)
input("Press Enter to continue...")
print("Try to write \"Hi from test1!\" from medium.txt")
x.mynfs_write(z2,"Hi from test1!")
input("Press Enter to continue...")



