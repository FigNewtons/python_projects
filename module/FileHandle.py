class File:
    def __init__(self, filename):
        self.line_pos = [0]
        self.lines = []
        self._cache(filename)
    
    def _cache(self, filename):
        try:
            with open(filename, 'rb+') as f:
                for line in f:
                    self.line_pos.append(f.tell())
                    self.lines.append(line)
        except FileNotFoundError:
            print('Error: ' + filename + ' not found')
    
    def pprint(self):
        for line_no, line in enumerate(self.lines):
            print(line_no, line.decode())
    
    def printline(self, line_no = 1):
        try:
            print(self.lines[line_no - 1])
        except IndexError:
            print('Error: Line number out of range')
    
    def printlines(self, start = 0, num_lines = 10):
        try:
            for line in self.lines[start: start + num_lines]:
                print(line.decode())
        except IndexError:
            print('Error: Out of range')
            print('Check starting position or number of lines requested')
    
    def getline(self, line_no = 1):
        try:
            return self.lines[line_no - 1]
        except IndexError:
            print('Error: Line number out of range')
            return None
    
    
