#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from library.general import *

msg = "Chess algorithms as an example Programming a Computer for Playing Chess was a 1950 paper that evaluated a minimax algorithm that is part of the history of algorithmic complexity; a course on IBM's Deep Blue (chess computer) is part of the computer science curriculum at Stanford University."


x = input("Enter the server's IP address: ")
buffer_size = 10
chace_size = 10
timeout = 300
x = General(x,12001,buffer_size,chace_size,timeout)

z = x.mynfs_open("empty.txt", O_WRONLY)

x.mynfs_write(z,"Hello World!")
input("Press Enter to continue...")
x.mynfs_seek(z,0)
input("Press Enter to continue...")
x.mynfs_write(z,10)
input("Press Enter to continue...")
tmp = input("Write something to the file: ")
x.mynfs_write(z,tmp)
input("Press Enter to continue...")
x.mynfs_seek(z,50)
input("Press Enter to continue...")
x.mynfs_truncate(z,10)
input("Press Enter to continue...")
x.mynfs_write(z,msg)
input("Press Enter to continue...")
x.mynfs_truncate(z,400)
