
from cell import Cell

class FastCell(Cell):

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
