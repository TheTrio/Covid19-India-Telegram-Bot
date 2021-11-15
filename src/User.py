from Tree import Tree

class User:
    def __init__(self,fname,lname,username):
        self.fname = fname
        self.lname = lname
        self.username = username
        self.help_mode = False
        self.tree = Tree()
        self.query_string = ''