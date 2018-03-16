from cell import Cell
from random import randint, shuffle

class Generation(object):

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
        :return:
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
        for row in self.cells():
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
        #TODO: Remove this error that exists to talk about debugging.
#        self._cells = self.create_cells()
        self.create_cells()
        cellLocations = [(cell.row, cell.column) for cell in self.cells()]
        shuffle(cellLocations)
        numberToLive = int( len(self) * (percentAlive/100) )
        for _ in range(numberToLive):
            row, column = cellLocations.pop()
            self._cells[row][column].live()





def xtest_world():
    w = Generation(10, 10)
    print(w)
    w.initial_populate_cells(10)
    print(w)
    w.initial_populate_cells(50)
    print(w)
    w.initial_populate_cells(100)
    print(w)
    w.initial_populate_cells(0)
    print(w)
    w = Generation(2, 8)
    print(w)
    w._cells[0][0].live()
    print(w)
    w._cells[1][7].live()
    print(w)
    w.initial_populate_cells(50)
    print(w)
    w.populate_cells(50)
    print(w)
    w = Generation(9, 3)
    w.populate_cells(50)
    print(w)
    w = Generation(24, 80)
    # for _ in range(500):
    #     w.better_populate_cells(25)
    #     print(w)

def xtest_neighbors():
    w = Generation(5, 5)
    w._cells[1][2].live()
    w._cells[2][2].live()
    w._cells[3][2].live()
    print(w)
    assert w.neighbors(w._cells[1][1]) == 2
    assert w.neighbors(w._cells[1][2]) == 1
    assert w.neighbors(w._cells[1][3]) == 2
    assert w.neighbors(w._cells[2][1]) == 3
    assert w.neighbors(w._cells[2][2]) == 2
    assert w.neighbors(w._cells[2][3]) == 3
    assert w.neighbors(w._cells[3][1]) == 2
    assert w.neighbors(w._cells[3][2]) == 1
    assert w.neighbors(w._cells[3][3]) == 2

    for row in range(1,4):
        for column in range(1,4):
            print(f'cells[{row}][{column}]: {w.neighbors(w.cells[row][column])} neighbors')
