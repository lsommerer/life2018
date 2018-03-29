class Cell(object):

    displayCharacters = 'squares'

    if displayCharacters  == 'circles':
        liveChar = '\u26AB'
        deadChar = '\u26AA'

    if displayCharacters  == 'squares':
        liveChar = '\u2B1B'
        deadChar = '\u2B1C'

    if displayCharacters  == 'soccer':
        liveChar = '\u26BD'
        deadChar = '\u2B1C'

    if displayCharacters  == 'basic':
        liveChar = 'O'
        deadChar = '.'

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
        if self.alive:
            state = 'alive'
        else:
            state = 'dead'
        return f'Cell[{self.row}][{self.column}]:{state}'

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

    def next_state(self, rules):
        neighbors = self.living_neighbors()
        nextState = False
        if self.alive:
            if neighbors in rules[0]:
                nextState = True
        else:
            if neighbors in rules[1]:
                nextState = True
        return nextState