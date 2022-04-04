class Group:
    def __init__(self, group_name):
        self.group_name: String = group_name
        self.members: Process_Info = []

    def add_member(self, member):
        self.members.append(member)

    def get_members(self):
        return self.members

    def find_members(self, member):
        for x in range(len(self.members)):
            if self.members[x].process_name == member.process_name and self.members[x].host == member.host and self.members[x].port == member.port:
                return x
        return None

    def remove_member(self, x):
        tmp = self.members[x]
        self.members.remove(tmp)

    def get_name(self):
        return self.group_name

    def toString(self):
        str = self.group_name
        for member in self.members:
            str += "#" + member.toString()
        return str


class Group_List:
    def __init__(self):
        self.groups: Group = []

    def add_group(self, group):
        self.groups.append(group)

    def find_group(self, group_name):
        for group in self.groups:
            if group.group_name == group_name:
                return group
        return None

    def remove_group(self, group):
        self.groups.remove(group)



class Process_Info:
    def __init__(self, process_name, host, port: int):
        self.process_name = process_name
        self.host = host
        self.port = port

    def toString(self):
        return self.process_name + " " + self.host + " " + str(self.port)

