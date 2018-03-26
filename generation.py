from cell import Cell
from random import randint, shuffle

class Generation(object):

    deadASCII = '.'
    aliveASCII = 'x'

    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns
        self.create_cells()
        self.assign_neighbors()

    def __str__(self):
        string = ''
        for row in self._cells:
            string += '\n'
            for cell in row:
                string += str(cell)
        return string

    def __len__(self):
        return self.rows * self.columns

    def create_cells(self):
        self._cells = []
        for row in range(self.rows):
            self._cells.append([])
            for column in range(self.columns):
                self._cells[row].append(Cell(row, column))

    def cells(self):
        for row in self._cells:
            for cell in row:
                yield cell

    def assign_neighbors(self):
        """
        Each cell has a list of all of it's neighbors. This is complicated by the fact that
        the cells on the edge of the world do not have as many neighbors as the cells in the
        middle of the world.
        """
        topRow = 0
        bottomRow = self.rows - 1
        leftMostColumn = 0
        rightMostColumn = self.columns - 1

        for cell in self.cells():
            #
            # All of the possible neighbor's coordinates
            #
            neighbors = [(-1,-1), (-1, 0), (-1, 1),
                         (0, -1),          (0, 1),
                         (1, -1), (1, 0),  (1, 1)]
            #
            # "python remove item from list and ignore index errors"
            #
            neighbors = set(neighbors)
            #
            # Discard the ones that don't work for the outer edge of the world.
            #
            if cell.row == topRow:
                neighbors.discard((-1, -1))
                neighbors.discard((-1, 0))
                neighbors.discard((-1, 1))
            if cell.row == bottomRow:
                neighbors.discard((1, -1))
                neighbors.discard((1, 0))
                neighbors.discard((1, 1))
            if cell.column == leftMostColumn:
                neighbors.discard((-1, -1))
                neighbors.discard((0, -1))
                neighbors.discard((1, -1))
            if cell.column == rightMostColumn:
                neighbors.discard((-1, 1))
                neighbors.discard((0, 1))
                neighbors.discard((1, 1))
            #
            # Add the remaining neighbors to the cell's list of neighbors
            #
            for neighbor in neighbors:
                neighborRow = cell.row + neighbor[0]
                neighborColumn = cell.column + neighbor[1]
                cell.neighbors.append(self._cells[neighborRow][neighborColumn])

    def count_living(self):
        countLiving = 0
        for cell in self.cells():
            if cell.alive:
                countLiving += 1
        return countLiving

    def initial_populate_cells(self, percentAlive=30):
        """
        Makes a certain percentage of the cells in the world alive. Note that this isn't
        a very good way to do this. You get about what you want for percentage, but not
        the actual amount. Look at populate_cells() for a better implementation.
        """
        for cell in self.cells():
            if randint(1, 101) <= percentAlive:
                cell.live()

    def populate_cells(self, percentAlive=30):
        """
        Populate cells by creating a list of all possible cells, shuffling that list, and
        picking the first X cells from the list to change to alive. X is the percentAlive
        argument times the total number of cells in the generation.

        :param percentAlive: Percentage of cells in this generation that will be changed to alive.
        :return:
        """
        #TODO: Remove this error that I left so that we could talk about the debugger.
        #
        # Originally, I had init working just like below with a call to create_cells().
        # That worked fine, and populate_cells() worked fine as well. But I changed
        # create_cells() so that it took care of creating self._cells and didn't return
        # anything. Then I didn't run my unit tests for some time, so I didn't know
        # why I was getting an error in some unrelated function.
        #
        # Uncomment the line below and run the unit test to see the error. I had to become
        # familiar with the pyCharm debugger to fix this, and so I think it will be a
        # good intro to the pyCharm debugger.
        #
        #self._cells = self.create_cells()
        cellLocations = [(cell.row, cell.column) for cell in self.cells()]
        shuffle(cellLocations)
        numberToLive = int( len(self) * (percentAlive/100) )
        for _ in range(numberToLive):
            row, column = cellLocations.pop()
            self._cells[row][column].live()

    def next_generation(self):
        #TODO See if deepcopy is faster than creating a new generation
        nextGeneration = Generation(self.rows, self.columns)
        for cell in self.cells():
            if cell.next_state():
                nextGeneration._cells[cell.row][cell.column].live()
        return nextGeneration

    def as_text(self, alive='x', dead='.'):
        """
        Returns the generation as a text string
        :param alive: Character to use for the alive cells
        :param dead: Character to use for the dead cells
        :return: A string suitable for saving to a text file.
        """
        string = ''
        for row in self._cells:
            string += '\n'
            for cell in row:
                if cell.alive:
                    string += Generation.aliveASCII
                else:
                    string += Generation.deadASCII
        return string


















