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

print("Open test.c")
z1 = x.mynfs_open("test.c", O_RDWR)
print("Open test1.txt")
z2 = x.mynfs_open("test1.txt", O_RDONLY)


print("Read 10 bytes from test.c")
print(x.mynfs_read(z1,10))
input("Press Enter to continue...")
print("Read 10 bytes from test1.txt")
print(x.mynfs_read(z2,10))
input("Press Enter to continue...")
print("Read 10 bytes from test.c")
print(x.mynfs_read(z1,10))
input("Press Enter to continue...")
print("Read 10 bytes from test1.txt")
print(x.mynfs_read(z2,10))
input("Press Enter to continue...")
print("Write \"Hi from test1!\" from test.c")
x.mynfs_write(z1,"Hello World!")
input("Press Enter to continue...")
print("Seek to the beginning of test.c and read 50 bytes")
x.mynfs_seek(z1,0,0)
print(x.mynfs_read(z1,50))
input("Press Enter to continue...")
print("Read 10 bytes from test1.txt")
print(x.mynfs_read(z2,20))
input("Press Enter to continue...")
print("Seek to the 50th byte of test1.txt and write 10")
x.mynfs_seek(z2,50,0)
x.mynfs_write(z2,10)
input("Press Enter to continue...")



