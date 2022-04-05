import threading
import socket
import sys  
import os


class CATOC_RM:
    def __init__(self, grp):
        self.pids = grp
        self.seqno = 0
        self.mids = []
        self.mbuf = []
        #self.delivered = [len(self.pids)]
        self.mypid = os.getpid()
        self.myvote = 0
        

    def CATOC_RM_send(self, msg):
        self.seqno = self.seqno + 1
        maxvote = 0
        vote = 0
        vpid = 0
        data = "TRM-MSG " + str(self.mypid) + "." + str(self.seqno) + " " + msg
        for pid in self.pids:
            send(pid, data)
        for pid in self.pids:
            receive(pid, vote)
            if vote > maxvote or vote == maxvote and pid > vpid:
                maxvote = vote
                vpid = pid
        data = "TRM-SEQ " + str(self.mypid) + "." + str(self.seqno) + " " + str(maxvote) + "." + str(vpid)
        for pid in self.pids:
            send(pid, data)
    
    def Causal_RM_deliver(self, msg):
        if msg[0] == "CRM-MSG":
            self.myvote = self.myvote + 1
            x = message(msg.split(" ")[1], self.myvote, "?",msg.split(" ")[3])
            self.mbuf.append(x)
            data = "CRM-VOTE " + str(self.mypid) + "." + str(self.seqno) + " " + str(self.myvote)
            send(pid, data)
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
                return (msg.split(" ")[2])



class message:
    def __init__(self, pid, myvote, vote , msg):
        self.msg = msg
        self.myvote = myvote
        self.vote = vote
        self.pid = pid