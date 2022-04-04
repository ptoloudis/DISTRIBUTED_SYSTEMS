from Group import Group, Process_Info

class list_node:
    def __init__(self, id, group: Group, value):
        self.id = id
        self.group = group
        self.value: int = value
    def get_value(self):
        return self.value
    def get_group(self):
        return self.group.get_name()
    def get_id(self):
        return self.id
    def set_group(self, group: Group):
        self.group = group
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

def replace_group(list, group):
    for node in list:
        if node.get_group == group.get_name():
            node.set_group(group)