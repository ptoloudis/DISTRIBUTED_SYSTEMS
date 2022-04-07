import threading
import socket
import sys  
import os

send_msq: msq = []
resive_msq: msq = []
resive_vote: msq = []
resive: msq = []

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

    def CATOC_RM_send(self, msg):
        global send_msq, resive_msq
        self.seqno = self.seqno + 1
        maxvote = 0
        vote = 0
        vpid = 0
        data = "TRM-MSG " + str(self.mypid) + "." + str(self.seqno) + " " + msg
        for pid in self.pids:
            tmp = msq(pid, data)
            send_msq.append(tmp)
        for pid in self.pids:
            resive_vote.pop(pid)
            if vote > maxvote or vote == maxvote and pid > vpid:
                maxvote = vote
                vpid = pid
        data = "TRM-SEQ " + str(self.mypid) + "." + str(self.seqno) + " " + str(maxvote) + "." + str(vpid)
        for pid in self.pids:
            tmp = msq(pid, data)
            send_msq.append(tmp)
    
    def Causal_RM_deliver(self):
        global resive
        while True:
            if len(resive) > 0:
                for msg in resive:
                    if msg[0] == "CRM-MSG":
                        self.myvote = self.myvote + 1
                        x = message(msg.split(" ")[1], self.myvote, "?",msg.split(" ")[3])
                        self.mbuf.append(x)
                        data = "CRM-VOTE " + str(self.mypid) + "." + str(self.seqno) + " " + str(self.myvote)
                        tmp = msq(x.get_pid(), data)
                        send_msq.append(tmp)
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
                    resive_msq.append(msg.split(" ")[2])

    def Recive(self):
        return resive_msq.pop(0)

class message:
    def __init__(self, pid, myvote, vote, msg):
        self.msg = msg
        self.myvote = myvote
        self.vote = vote
        self.pid = pid
    def get_pid(self):
        return self.pid

class msq:
    def __init__(self, pid: Pids, msg):
        self.pid = pid
        self.msg = msg
    def get_pid(self):
        return self.pid


def UDP_send(sock):
    global send_msq, resive_msq, resive_vote
    while True:
        try:
            if len(send_msq) > 0:
                msg = send_msq.pop(0)
                pid = msg.get_pid()
                sock.sendto(msg.msg.encode(), (pid.get_host(), pid.get_port()))
            else:
                sock.settimeout(2)
                try:
                    tmp = sock.recvfrom(1024)
                    resive.append(tmp)
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            return 0