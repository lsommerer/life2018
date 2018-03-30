from fastcell import FastCell
from generation import Generation
from random import shuffle

class FastGeneration(Generation):

    def __init__(self, rows, columns, geometry='dish', rules=[[2,3],[3]]):
        super().__init__(rows, columns, geometry, rules)
        self.livingCells = []

    def create_cells(self):
        self._cells = []
        for row in range(self.rows):
            self._cells.append([])
            for column in range(self.columns):
                self._cells[row].append(FastCell(row, column, self))

    def populate_cells(self, percentAlive=30):
        """
        Populate cells by creating a list of all possible cells, shuffling that list, and
        picking the first X cells from the list to change to alive. X is the percentAlive
        argument times the total number of cells in the generation.

        :param percentAlive: Percentage of cells in this generation that will be changed to alive.
        :return:
        """
        cellLocations = [(cell.row, cell.column) for cell in self.cells()]
        shuffle(cellLocations)
        numberToLive = int( len(self) * (percentAlive/100) )
        for _ in range(numberToLive):
            row, column = cellLocations.pop()
            self._cells[row][column].live()
            self.livingCells.append((row, column))

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
            cell.neighbors = []
            for neighbor in neighbors:
                neighborRow = (cell.row + neighbor[0])
                neighborColumn = (cell.column + neighbor[1])
                cell.neighbors.append((neighborRow, neighborColumn))

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
            cell.neighbors = []
            for neighbor in neighbors:
                neighborRow = (cell.row + neighbor[0]) % self.rows
                neighborColumn = (cell.column + neighbor[1]) % self.columns
                cell.neighbors.append((neighborRow, neighborColumn))


    def next_generation(self):
        #DONE See if deepcopy is faster than creating a new generation
        #     It is much, much slower.
        nextGeneration = FastGeneration(self.rows, self.columns, self.geometry, self.rules)
        for cell in self.cells():
            nextGeneration._cells[cell.row][cell.column].neighbors = cell.neighbors
            if cell.next_state(self.rules):
                nextGeneration._cells[cell.row][cell.column].live()
            else:
                nextGeneration._cells[cell.row][cell.column].die()
        return nextGeneration

    def next_generation2(self):
        #DONE See if deepcopy is faster than creating a new generation
        #     It is much, much slower.
        nextGeneration = FastGeneration(self.rows, self.columns, self.geometry, self.rules)
        newLivingCells = []
        for cell in self.livingCells:
            nextGeneration._cells[cell.row][cell.column].neighbors = cell.neighbors
            if cell.next_state(self.rules):
                nextGeneration._cells[cell.row][cell.column].live()
            else:
                nextGeneration._cells[cell.row][cell.column].die()
        return nextGeneration

















