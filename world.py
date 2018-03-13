from cell import Cell
from random import randint, shuffle

class World(object):

    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns
        self.cells = self.create_cells()


    def __str__(self):
        string = ''
        for row in self.cells:
            string += '\n'
            for cell in row:
                string += str(cell)
        return string


    def __len__(self):
        return self.rows * self.columns

    def create_cells(self):
        cells = []
        for row in range(self.rows):
            cells.append([])
            for column in range(self.columns):
                cells[row].append(Cell(row, column))
        return cells

    def populate_cells(self, percentAlive=30):
        """Makes a certain percentage of the cells in the world alive."""
        for row in self.cells:
            for cell in row:
                if randint(1, 101) <= percentAlive:
                    cell.live()

    def better_populate_cells(self, percentAlive=30):
        self.cells = self.create_cells()
        cellLocations = [(row, column) for row in range(self.rows) for column in range(self.columns)]
        shuffle(cellLocations)
        numberToLive = int( len(self) * (percentAlive/100) )
        for _ in range(numberToLive):
            row, column = cellLocations.pop()
            self.cells[row][column].live()

    def neighbors(self, cell):
        """Returns the number of living neighbors a cell has."""
        neighbors = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                neighbors +=  self.cells[cell.row+y][cell.column+x].alive
        if self.cells[cell.row][cell.column].alive:
            neighbors -= 1
        return neighbors



def xtest_world():
    w = World(10, 10)
    print(w)
    w.populate_cells(10)
    print(w)
    w.populate_cells(50)
    print(w)
    w.populate_cells(100)
    print(w)
    w.populate_cells(0)
    print(w)
    w = World(2,8)
    print(w)
    w.cells[0][0].live()
    print(w)
    w.cells[1][7].live()
    print(w)
    w.populate_cells(50)
    print(w)
    w.better_populate_cells(50)
    print(w)
    w = World(9,3)
    w.better_populate_cells(50)
    print(w)
    w = World(24, 80)
    # for _ in range(500):
    #     w.better_populate_cells(25)
    #     print(w)

def xtest_neighbors():
    w = World(5, 5)
    w.cells[1][2].live()
    w.cells[2][2].live()
    w.cells[3][2].live()
    print(w)
    assert w.neighbors(w.cells[1][1]) == 2
    assert w.neighbors(w.cells[1][2]) == 1
    assert w.neighbors(w.cells[1][3]) == 2
    assert w.neighbors(w.cells[2][1]) == 3
    assert w.neighbors(w.cells[2][2]) == 2
    assert w.neighbors(w.cells[2][3]) == 3
    assert w.neighbors(w.cells[3][1]) == 2
    assert w.neighbors(w.cells[3][2]) == 1
    assert w.neighbors(w.cells[3][3]) == 2

    for row in range(1,4):
        for column in range(1,4):
            print(f'cells[{row}][{column}]: {w.neighbors(w.cells[row][column])} neighbors')
