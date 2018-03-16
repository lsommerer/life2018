class Cell(object):

    liveChar = '\u26AB'
    deadChar = '\u26AA'

    def __init__(self, row, column):
        self.alive = False
        self.row = row
        self.column = column
        self.neighbors = []

    def __str__(self):
        if self.alive:
            return Cell.liveChar
        else:
            return Cell.deadChar

    def __repr__(self):
        return f'Cell[{self.row}][{self.column}]:{self.alive}'

    def live(self):
        self.alive = True
        return self

    def die(self):
        self.alive = False
        return self

    def living_neighbors(self):
        """Returns the number of living neighbors a cell has."""
        livingNeighbors = 0
        for neighbor in self.neighbors:
            if neighbor.alive:
                livingNeighbors += 1
        return livingNeighbors
