class Group:
    def __init__(self, group_name):
        self.group_name = group_name
        self.members: Process_Info = []

    def add_member(self, member):
        self.members.append(member)

    def get_members(self):
        return self.members

    def find_members(self, member):
        return member in self.members

    def remove_member(self, member):
        self.members.remove(member)

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
    def __init__(self, process_name, host, port):
        self.process_name = process_name
        self.host = host
        self.port = port

    

