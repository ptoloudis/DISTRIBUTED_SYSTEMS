import threading
from buffer_cl import *


def send(self,svcid, reqbuf, reqlen, resbuf, reslen):
    tmp = messeges(svcid, reqbuf, reqlen)
    id = tmp.return_id()
    self.send_buffer.add(tmp)
    tmp = self.re_buffer.get(id)
    resbuf = tmp.messege
    reslen = tmp.messege_length

def send_messeger():
    while True:
        tmp = send_buffer.get()
        #unpack(tmp.messege)
        #TODO: send messege
        #
        #TODO: receive messege
        #
        #pack the messege
        re_buffer.add(tmp)


## MAIN ##
send_buffer = buffer_send(10)
re_buffer = buffer_re(10)
id()
transport = False
x = threading.Thread(send_messeger)
x.start()
