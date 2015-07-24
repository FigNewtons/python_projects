from itertools import accumulate as acc

class File:
    def __init__(self, filename):
        self.filename = filename
        self.line_pos = [0]
        self.lines = []
        self._cache(filename)
    
    
    def _cache(self, filename):
        try:
            with open(filename, 'rb+') as f:
                for line in f:
                    self.line_pos.append(f.tell())
                    self.lines.append(line.decode())
        except FileNotFoundError:
            print('Error: ' + filename + ' not found')
    
    
    def pprint(self):
        """Print entire file with line numbers; properly formatted. """
        for line_no, line in enumerate(self.lines):
            print(line_no + 1, line)
    
    
    def printline(self, line_no = 1):
        """Print a specified line from the file. """
        try:
            print(self.lines[line_no - 1])
        except IndexError:
            print('Error: Line number out of range')
    
    
    def printlines(self, start = 1, num_lines = 10):
        """Print a block of lines from the line, given a starting line. """
        try:
            start -= 1
            for line in self.lines[start : start + num_lines]:
                print(line)
        except IndexError:
            print('Error: Out of range')
            print('Check starting position or number of lines requested')
    
    
    def getline(self, line_no = 1):
        """Return a specified line. """
        try:
            return self.lines[line_no - 1]
        except IndexError:
            print('Error: Line number out of range')
            return None
    
    
    def insert(self, text, line_no = 'end'):
        """Insert a piece of text (containing possibly many lines) to
        the file starting at the specified line number. Any existing 
        text is pushed down. """
        
        text_lines = text.split('\n')
        text_lines = [line + '\n' for line in text_lines]
        
        # Add one for the extra newline char added
        offset = len(text) + 1
        try:
            if line_no == 'end':
                line_no = len(self.lines)
            
            self.lines = self.lines[0: line_no - 1] + text_lines +  self.lines[line_no - 1: ]
            self.line_pos = [0] + list(acc([len(line) for line in self.lines]))
            
            current_pos = self.line_pos[line_no - 1]
            
            with open(self.filename, 'r+') as f:
                f.seek(current_pos)
                for i in range(line_no - 1, len(self.lines)):
                    f.write(self.lines[i])
        except IndexError:
            print('Error: line number out of range')
    
    
    def append(self, string, line_no = 'end'):
        """Append a string to the file at the specified line number. 
        By default, the function appends the last line (no newline included). 
        The string cannot contain any newlines. """
        if '\n' in string:
            print('Error: Cannot append; string contains newline')
        else:
            try:
                if line_no == 'end':
                    line_no = len(self.lines)
                
                line = self.lines[line_no - 1]
                appended_line = line[:-1] + string + '\n'
                # Replace line
                self.lines[line_no -1] = appended_line
                
                # Start at beginning of line
                current_pos = self.line_pos[line_no - 1]
                
                with open(self.filename, 'r+') as f:
                    f.seek(current_pos)
                    for i in range(line_no - 1, len(self.lines)):
                        f.write(self.lines[i])
                        self.line_pos[i + 1] += len(string)
                        
            except IndexError:
                print('Error: line number out of range')

