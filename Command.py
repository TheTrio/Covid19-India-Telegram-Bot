from Token import Token
class Command:
    def __init__(self, command, countries=[]):
        self.command = list(dict.fromkeys(command))
        self.countries = countries
    def is_sorted(self):
        for i in range(0,len(self.command)-1):
            if self.command[i].priority > self.command[i+1].priority:
                return False
        return True
    def get_sorted_command(self):
        if self.is_sorted():
            return self
        return Command(sorted(self.command,key=lambda token: token.priority))
    def convert(self):
        if len(self.countries)!=0 and len(self.command)>=1 and 'world' in self.command and 'new' in self.command:
            self.command = [Token('daily'), Token('World'), Token('new')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'world' in self.command and 'total' in self.command:
            self.command = [Token('daily'), Token('World'), Token('total')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'weekly' in self.command:
            if 'india' in self.command:
                self.countries.append('India')
            self.command = [Token('weekly'), Token('line')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'world' in self.command:
            if 'india' in self.command:
                self.countries.append('India')
            self.command = [Token('daily'), Token('World'), Token('new')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'world' in self.command and 'total' in self.command:
            if 'india' in self.command:
                self.countries.append('India')
            self.command = [Token('daily'), Token('World'), Token('new')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'india' in self.command and 'new' in self.command:
            self.command = [Token('daily'), Token('India'), Token('new')]
        elif len(self.countries)==0 and len(self.command)>=1 and 'india' in self.command and 'new' in self.command:
            self.command = [Token('daily'), Token('India'), Token('new')]
            self.countries = ['TT']
        elif len(self.countries)!=0 and len(self.command)>=1 and 'india' in self.command and 'total' in self.command:
            self.command = [Token('daily'), Token('India'), Token('total')]
        elif len(self.countries)==0 and len(self.command)>=1 and 'india' in self.command and 'total' in self.command:
            self.command = [Token('daily'), Token('India'), Token('total')]
            self.countries = ['TT']
        elif len(self.countries)==0 and len(self.command)>=1 and 'bar' in self.command:
            self.command = [Token('weekly'), Token('bar')]
        elif len(self.countries)==0 and len(self.command)>=1 and 'weekly' in self.command:
            self.command = [Token('weekly'), Token('bar')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'line' in self.command:
            if 'india' in self.command:
                self.countries.append('India')
            self.command = [Token('weekly'), Token('line')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'india' in self.command:
            self.command = [Token('daily'), Token('India'), Token('new')]
        elif len(self.countries)!=0 and len(self.command)>=1 and 'new' in self.command:
            self.command = [Token('daily'), Token('India'), Token('new')]
        
    def get_str(self):
        out_str = ''
        for token in self.command:
            out_str+=token.name + ' '
        return out_str.strip()