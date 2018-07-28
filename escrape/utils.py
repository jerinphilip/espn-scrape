class takeWhileLength:
    def __init__(self, seq, max_limit):
        self.delim = '\n'
        self.max_limit = max_limit
        self.seq = seq
        self.index = 0
        self.reset()
    
    def reset(self):
        self.count = 0
        self.seq_length = 0
        self.current = []
        
    
    def full(self):
        if self.index >= len(self.seq):
            return True
        current = len(self.seq[self.index])
        tentative = self.seq_length + current + len(self.delim)*self.count
        return tentative > self.max_limit
    
    def advance(self):
        self.seq_length += len(self.seq[self.index])
        self.current.append(self.seq[self.index])
        self.index += 1
        self.count += 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while not self.full():
            self.advance()
        if not self.current:
            raise StopIteration
        
        export = self.delim.join(self.current)
        #print(len(export))
        self.reset()    
        assert(len(export) < self.max_limit)
        return export