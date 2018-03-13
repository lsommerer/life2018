class Cell(object):

    def __init__(self, row, column):
        self.alive = False
        self.row = row
        self.column = column
        self.liveChar = '\u26AB'
        self.deadChar = '\u26AA'

    def __str__(self):
        if self.alive:
            return self.liveChar
        else:
            return self.deadChar

    def live(self):
        self.alive = True
        return self

    def die(self):
        self.alive = False
        return self
