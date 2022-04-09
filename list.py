#
# Team : 1
# Names : Apostolopoulou Ioanna & Toloudis Panagiotis
# AEM : 03121 & 02995
#

from Group import Group, Process_Info

class list_node:
    def __init__(self, id, group: Group, value, pids):
        self.id = id
        self.group = group
        self.value: int = value
        self.pids = pids
    def get_value(self):
        return self.value
    def get_group(self):
        return self.group.get_name()
    def get_id(self):
        return self.id
    def set_group(self, group: Group):
        self.group = group
    def set_pids(self, pids):
        self.pids = pids
    def get_pids (self):
        return self.pids
    def toString(self):
        return self.id + " " + self.group.toString() + " " + str(self.value)

def find_node(list, id):
    for node in list:
        if node.value == id:
            return node
    return None

def add_group(Name, view):
    tmp = Group(Name)
    view = view[len(Name)+1:]
    x = True
    while x:
        name = view.split(" ")[0]
        host = view.split(" ")[1]
        view = view[len(name) + len(host) + 2:]
        port = view[:5]
        view = view[6:]
        if len(view) == 0:
            x = False
        member = Process_Info(name, host, port)
        tmp.add_member(member)
    return tmp

def replace_group(list, group, pids):
    for node in list:
        if node.get_group == group.get_name():
            node.set_group(group)
            node.set_pids(pids)


def add_pids(group: Group):
    pids = []
    members = group.get_members()
    for tmp in members:
        pid = Pids(tmp.get_host(), tmp.get_port())
        pids.append(pid)
    return pids

class Pids:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def get_host(self):
        return self.host
    def get_port(self):
        return self.port