class Node:
    def __init__(self, name, help,command=None):
        self.name = name
        self.children = []
        self.command = command
        self.help = help
        if command==None:
            self.command = self.name
    def __str__(self):
        return self.name
    def getHelp(self):
        return f'*{self.name}* \- _{self.help}_'