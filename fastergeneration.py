from generation import Generation
from random import shuffle

class FasterGeneration(Generation):
    """
    This version of Generation incorporates several efficiency improvements, often with a reduction
    in readability:

    After a few generations, most worlds tend to have over 85% dead cells. Most of these cells have
    no chance of coming alive in the next generation. So instead of keeping track of all of the cells,
    lets just keep a list of the living cells. To compute the next generation we only have to look at
    the living cells and their neighbors (which we are keeping track of anyway). Note that, because
    we don't want to compute a cell's neighbors when it becomes alive, we precompute the neighbors for
    every cell and keep it around for reference.

    This produced a modest increase in speed, but not what I was hoping for. It was very time consuming
    to figure out the number of living neighbors a cell had by doing:

    for cell in neighbors:
        if cell in livingCells:
            neighbors += 1

    It's faster to see if something is a member of a set than a list, especially a frozen set. To do
    that the cells would have to be immutable, so they are now a (row, column) tuple instead of an
    object. This resulted in a dramatic increase in speed.

    But if you're going to use sets, why not go all the way. The neighbors of a cell can also be a
    frozen set. So you can find the number of neighbors a cell has by counting the number of cells
    in the intersection of the neighbor set and the set of living cells:

    livingNeighbors = len(neighborSet & livingCells)

    Doesn't that sound like it would be slow? It is really fast. Here are the times:

    Generation:       252 seconds
    FastGeneration:   152 seconds
    FasterGeneration:  46 seconds

    I eaked another second off the time by using the join method instead of concatenation in the
    string method.
    """

    def __init__(self, rows, columns, geometry='dish', rules=[[2,3],[3]]):
        super().__init__(rows, columns, geometry, rules)
        self.neighborsList = []
        self.livingCells = []

    def __str__(self):
        stringList = []
        #
        # Craete a list where all the cells are dead.
        #
        for row in range(self.rows):
            stringList.append([])
            for column in range(self.columns):
                stringList[row].append(FasterGeneration.deadASCII)
        #
        # Turn the living ones alive.
        #
        row = 0
        column = 1
        for cell in self.livingCells:
            stringList[cell[row]][cell[column]] = FasterGeneration.aliveASCII
        #
        # Create the actual string.
        #
        string = ''
        for row in stringList:
            string += '\n'
            string += ''.join([cell for cell in row])
        return string

    def create_cells(self):
        self._cells = []
        for row in range(self.rows):
            self._cells.append([])
            for column in range(self.columns):
                self._cells[row].append((row, column))

    def assign_neighbors(self):
        self.neighborsList = []
        for row in range(self.rows):
            self.neighborsList.append([])
            for column in range(self.columns):
                self.neighborsList[row].append(set())

        if self.geometry == 'dish':
            self.assign_neighbors_dish()
        else:
            self.assign_neighbors_torus()

    def assign_neighbors_dish(self):
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
            row = 0
            column = 1
            if cell[row] == topRow:
                neighbors.discard((-1, -1))
                neighbors.discard((-1, 0))
                neighbors.discard((-1, 1))
            if cell[row] == bottomRow:
                neighbors.discard((1, -1))
                neighbors.discard((1, 0))
                neighbors.discard((1, 1))
            if cell[column] == leftMostColumn:
                neighbors.discard((-1, -1))
                neighbors.discard((0, -1))
                neighbors.discard((1, -1))
            if cell[column] == rightMostColumn:
                neighbors.discard((-1, 1))
                neighbors.discard((0, 1))
                neighbors.discard((1, 1))
            #
            # Add the remaining neighbors to the cell's list of neighbors
            #
            for neighbor in neighbors:
                neighborRow = (cell[row] + neighbor[row])
                neighborColumn = (cell[column] + neighbor[column])
                self.neighborsList[cell[row]][cell[column]].add((neighborRow, neighborColumn))
            self.neighborsList[cell[row]][cell[column]] = frozenset(self.neighborsList[cell[row]][cell[column]])

    def assign_neighbors_torus(self):
        """
        Find each cell's neighbors and store them in a list to use when computing the next generations.
        """
        for cell in self.cells():
            #
            # The neighbor's relative coordinates
            #
            neighbors = [(-1,-1), (-1, 0), (-1, 1),
                         (0, -1),          (0, 1),
                         (1, -1), (1, 0),  (1, 1)]

            #
            # There is not a problem when the indicies are too small. A negative index is fine
            # in Python and actually wraps around to the other end of the list, which is what
            # we want.
            #
            # But there is a problem with adding 1 onto the end of the list, so after we find
            # the row, we mod it by the length of the row. if the list has 10 rows, list[9] is
            # fine, but list[10] causes an index out of range error. list[10 mod 10] is equal
            # to list[0] which is where we want to be in the list anyway.
            #
            row = 0
            column = 1
            for neighbor in neighbors:
                neighborRow = (cell[row] + neighbor[row]) % self.rows
                neighborColumn = (cell[column] + neighbor[column]) % self.columns
                self.neighborsList[cell[row]][cell[column]].add((neighborRow, neighborColumn))
            self.neighborsList[cell[row]][cell[column]] = frozenset(self.neighborsList[cell[row]][cell[column]])

    def count_living(self):
        return len(self.livingCells)

    def populate_cells(self, percentAlive=30):
        """
        Populate cells by creating a list of all possible cells, shuffling that list, and
        picking the first X cells from the list to change to alive. X is the percentAlive
        argument times the total number of cells in the generation.

        :param percentAlive: Percentage of cells in this generation that will be changed to alive.
        :return:
        """
        row = 0
        column = 1
        cellLocations = [(cell[row], cell[column]) for cell in self.cells()]
        shuffle(cellLocations)
        numberToLive = int( len(self) * (percentAlive/100) )
        self.livingCells = set()
        for _ in range(numberToLive):
            self.livingCells.add(cellLocations.pop())

    def next_state(self, cell):
        """
        This method originally was part of Cell, but there are no Cell objects in FasterGeneration,
        so I moved it here.
        """
        row = 0
        column = 1
        #neighbors is the length of the union of the cell's neighbors and all living cells.
        neighbors = len(self.neighborsList[cell[row]][cell[column]] & self.livingCells)
        nextState = False
        if cell in self.livingCells:
            if neighbors in self.rules[0]:
                nextState = True
        else:
            if neighbors in self.rules[1]:
                nextState = True
        return nextState

    def next_generation(self):
        #DONE See if deepcopy is faster than creating a new generation
        #     It is much, much slower.
        row = 0
        column = 1
        #
        # We have to check the living cells and all of the cells surrounding them (their neighbors).
        # that would typically include a lot of duplicates, so we use a set instead of a list.
        #
        interestingCells = set()
        for cell in self.livingCells:
            interestingCells.add(cell)
            for neighbor in self.neighborsList[cell[row]][cell[column]]:
                interestingCells.add(neighbor)

        newLivingCells = []
        for cell in interestingCells:
            if self.next_state(cell):
                newLivingCells.append(cell)
        self.livingCells = frozenset(newLivingCells)
        #
        # We return self here because Simulation expects to get a generation back.
        #
        return self

    def as_text(self, alive='x', dead='.'):
        """
        Returns the generation as a text string
        :param alive: Character to use for the alive cells
        :param dead: Character to use for the dead cells
        :return: A string suitable for saving to a text file.
        """
        return str(self)


def test():
    f = FasterGeneration(6, 6)
    f.create_cells()
    f.populate_cells()
    print(f)
    f.assign_neighbors()
    print('dish')
    print(f.neighborsList[0][0])
    print(f.neighborsList[0][1])
    print(f.neighborsList[1][1])
    f.geometry = 'torus'
    f.assign_neighbors()
    print('torus')
    print(f.neighborsList[0][0])
    print(f.neighborsList[0][1])
    print(f.neighborsList[1][1])
    print(f)
    f.geometry = 'dish'
    f.assign_neighbors()
    f.next_generation()
    print(f)

if __name__ == '__main__':
    test()
















