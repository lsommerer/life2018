from cell import Cell
from generation import Generation
from random import shuffle

class FastGeneration(Generation):
    """
    It is VERY expensive to assign neighbors each time you create a new generation. So this version
    of Generation doesn't do that. It just copies the neighbors from the previous generation, because
    the neighbors don't change unless the geometry of the workd changes (in which case we do recompute
    the neighbors).

    Unfortunately, this means that we can no longer have the list of neighbors be a list of the
    actual cells, because the cells would be from the previous generation. So now the list of neighbors
    is just a list of the row and column that you can use to lookup the neighbor in the list of cells.

    This approach reduced the time to run the simulation by over 40 percent; nearly cutting the
    run time in half. The improvement is especially noticeable with larger worlds.
    """
    def __init__(self, rows, columns, geometry='dish', rules=[[2,3],[3]]):
        super().__init__(rows, columns, geometry, rules)

    def create_cells(self):
        self._cells = []
        for row in range(self.rows):
            self._cells.append([])
            for column in range(self.columns):
                self._cells[row].append(FastCell(row, column, self))

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
        nextGeneration = FastGeneration(self.rows, self.columns, self.geometry, self.rules)
        for cell in self.cells():
            nextGeneration._cells[cell.row][cell.column].neighbors = cell.neighbors
            if cell.next_state(self.rules):
                nextGeneration._cells[cell.row][cell.column].live()
            else:
                nextGeneration._cells[cell.row][cell.column].die()
        return nextGeneration



class FastCell(Cell):
    """
    A slight variation on the Cell class. Although it is very eligant for the cell to contain a list of
    all of its neighbors, It was really slowing things down, so in FastGeneration the cell has a list which
    contains the row and column of all of its neighbors. FastGeneration has a list of all of the cells and
    and FastCells has to have a reference to the generation to look those up.
    """

    def __init__(self, row, column, generation):
        super().__init__(row, column)
        self.generation = generation

    def living_neighbors(self):
        """Returns the number of living neighbors a cell has."""
        livingNeighbors = 0
        for neighbor in self.neighbors:
            if self.generation._cells[neighbor[0]][neighbor[1]].alive:
                livingNeighbors += 1
        return livingNeighbors















