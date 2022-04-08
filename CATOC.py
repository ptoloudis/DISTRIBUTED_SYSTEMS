from pickle import NONE
import threading
import socket
import sys  
import os
import time
from list import *

Buffer = None
send_msg = []
receive_msg = []
receive_msg_Fifo = []
receive_vote = []
receive = []

class CATOC_RM:
    def __init__(self, grp):
        self.pids = grp
        self.seqno = 0
        self.mids = []
        self.mbuf = []
        self.mypid = os.getpid()
        self.myvote = 0

    def set_pids(self, grp):
        self.pids = grp

    def CATOC_RM_send(self, message):
        global send_msg, receive_msg, receive_vote
        self.seqno = self.seqno + 1
        maxvote = 0
        vote = 0
        vpid = 0
        data = "TRM-MSG " + str(self.mypid) + "." + str(self.seqno) + " " + message
        for pid in self.pids:
            tmp = msg(pid, data)
            send_msg.append(tmp)
        for pid in self.pids:
            while len(receive_vote) == 0:
                continue
            receive_vote.pop(0)
            if vote > maxvote or vote == maxvote and pid > vpid:
                maxvote = vote
                vpid = pid
        data = "TRM-SEQ " + str(self.mypid) + "." + str(self.seqno) + " " + str(maxvote) + "." + str(vpid)
        for pid in self.pids:
            tmp = msg(pid, data)
            send_msg.append(tmp)
    
    def Causal_RM_deliver(self):
        global receive
        while True:
            if len(receive) > 0:
                for msg in receive:
                    if msg[0] == "CRM-MSG":
                        self.myvote = self.myvote + 1
                        x = message(msg.split(" ")[1], self.myvote, "?",msg.split(" ")[3])
                        self.mbuf.append(x)
                        data = "CRM-VOTE " + str(self.mypid) + "." + str(self.seqno) + " " + str(self.myvote)
                        tmp = msg(x.get_pid(), data)
                        send_msg.append(tmp)
                    if msg[0] == "CRM-VOTE":
                        vote = msg.split(" ")[2]
                        self.myvote = max(self.myvote, vote.split(".")[0])
                        x = message(msg.split(" ")[1], "*", vote, "*")
                        self.mbuf.append(x)
                        self.checkBuffer()

    def checkBuffer(self):
        if len(self.mbuf) > 0:
            for msg in self.mbuf:
                x = msg.split(".")[0]
                k = msg.split(".")[1]
                mmids = msg.split(" ")[2]
                if (k == self.delivered[x] + 1) and (mmids in self.mids):
                    self.mbuf.remove(msg)
                    self.mids =+ msg.split(" ")[1]
                    self.delivered[x] = k
                    receive_msg.append(msg.split(" ")[2])

class FIFO_RM:
    def __init__(self, grp):
        self.pids = grp
        self.seqno = 0
        self.mids = []
        self.mypid = os.getpid()
        self.mbuf = []
        self.delivered : int = [len(self.pids)]

    def FIFO_RM_send(self, message):
        self.seqno = self.seqno + 1
        data = "FIFO-MSG " + str(self.mypid) + "." + str(self.seqno) + " " + message
        for pid in self.pids:
            tmp = msg(pid, data)
            send_msg.append(tmp)

    def FIFO_RM_deliver(self):
        global receive_msg_Fifo
        while True:
            if len(receive_msg_Fifo) > 0:
                for msg in receive_msg_Fifo:                        
                    if msg.split(".")[0] not in self.mypid:
                        for pid in self.pids:
                            tmp = msg(pid, msg)
                            send_msg.append(tmp)
            
                    self.mbuf.append(msg[8:])
                    self.checkBuffer()

    def checkBuffer(self):
        if len(self.mbuf) > 0:
            for msg in self.mbuf:
                x = msg.split(".")[0]
                k = msg.split(".")[1]
                if k == self.delivered[x] + 1:
                    self.mbuf.remove(msg)
                    self.delivered[x] = k
                receive_msg.append(msg.split(" ")[2])

def Send_to_App(block):
    global receive_msg
    if block == 1:
        while True:
            if len(receive_msg) > 0:
                return (receive_msg.pop(0))
            else:
                time.sleep(0.1)
    else:
        if len(receive_msg) > 0:
            return (receive_msg.pop(0))
        else:
            return NONE

class message:
    def __init__(self, pid, myvote, vote, msg):
        self.msg = msg
        self.myvote = myvote
        self.vote = vote
        self.pid = pid
    def get_pid(self):
        return self.pid

class msg:
    def __init__(self, pid, data):
        self.pid = pid
        self.data = data
    def get_pid(self):
        return self.pid

def UDP_send(sock):
    global send_msg, receive_msg, receive_vote
    print("Sending messages")
    while True:
        try:
            if len(send_msg) > 0:
                data = send_msg.pop(0)
                pid = data.get_pid()
                print("Sending to " + str(pid) + ": " + data.data)
                sock.sendto(data.data.encode(), (pid.get_host(), pid.get_port()))
            else:
                sock.settimeout(1)
                try:
                    tmp = sock.recvfrom(1024)
                    print("Received: " + tmp.decode())
                    if tmp[0].decode()[0:7] == "FIFO-MSG":
                        receive_msg_Fifo.append(tmp[0].decode())
                    else:
                        receive.append(tmp[0].decode())
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            return 0
        