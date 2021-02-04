class Token:
    priorities = {
        'daily':1,
        'india':2,
        'total':3,
        'new':3,
        'world':2,
        'weekly':1,
        'bar':2,
        'line':2
    }
    def __init__(self, name):
        self.name = name.lower()
        if self.name in self.priorities:
            self.priority = self.priorities[self.name]
        else:
            self.priority = 5
    def __str__(self):
        return self.name
    def __eq__(self, other):
        if isinstance(other, str):
            return self.name==other
        return self.name==other.name
    def __hash__(self):
        return self.name.__hash__()