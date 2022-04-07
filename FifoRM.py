import grp
import socket
import threading
import time
import os
import sys



def TRM_Init(grp):
    RM-Init(grp)
    seqno = 0
    mbuf = []
    pids = grp
    myvote = 0
    mypid = os.getpid()

def TRM_send(msg):
    seqno = seqno + 1
    maxVote = 0 
    vpid = 0
    mbuf.append(msg)
    for pid in pids:
        if pid == mypid:
            continue
        send(pid, msg)
    for pid in pids:
        if pid == mypid:
            continue
        vote = recv(pid)
        if vote > maxVote:
            maxVote = vote
            vpid = pid
    if vpid == mypid:
        myvote = maxVote
    return myvote



# RM-send(<TRM-MSG, mypid.seqno, msg>)
# for each pid ∈ pids
# receive(pid,<TRM-VOTE, mypid.seqno, vote>)
# if vote > maxvote or vote = maxvote and pid > vpid
# maxvote, vpid ← vote, pid
# endif
# endfor
# RM-send(<TRM-SEQ, mypid.seqno, maxvote.vpid>)

# def RM-deliver():
#     myvote = myvote +1
#     mbuf = mbuf + [pid.k, myvote.mypid, "?", msg]
#     send(pid,<TRM-VOTE, pid.k, myvote.mypid>)

def RM_deliver(msg):
    myvote = max(myvote, seqno)
    mbuf.append(msg)




def checkBuffer():
    while True:
        if len(mbuf) > 0:
            msg = mbuf.pop(0)
            RM_deliver(msg)
        time.sleep(0.1)



    class RM:
#     def __init__(self, grp):
#         self.pids = grp
#         self.seqno = 0
#         self.mids = []
#         self.mypid = os.getpid()

#     def RM_send(self, msg):
#         self.seqno = self.seqno + 1
#         data = "RM-MSG " + str(self.mypid) + "." + str(self.seqno) + " " + msg
#         for pid in self.pids:
#             send(pid, data)

#     def RM_deliver(self, msg):
#         if msg[0] == "RM-MSG":
#             x = msg.split(" ")[1]
#             if x not in self.mids:
#                 self.mids.append(x)
#                 print(msg) 
#                 if x.split(".")[0] not in self.mypid:
#                     for pid in self.pids:
#                         send(pid, msg)
#         return (msg.split(" ")[2])
