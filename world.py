from cell import Cell
from random import randint, shuffle

class World(object):

    def __init__(self, rows, columns, percentAlive=30):

        self.rows = rows
        self.columns = columns
        self.cells = []
        self.create_cells()

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
        self.cells = []
        for row in range(self.rows):
            self.cells.append([])
            for column in range(self.columns):
                self.cells[row].append(Cell(row, column))

    def populate_cells(self, percentAlive=30):
        """Makes a certain percentage of the cells in the world alive."""
        for row in self.cells:
            for cell in row:
                if randint(1, 101) <= percentAlive:
                    cell.live()

    def better_populate_cells(self, percentAlive=30):
        self.create_cells()
        cellLocations = [(row, column) for row in range(self.rows) for column in range(self.columns)]
        shuffle(cellLocations)
        numberToLive = int( len(self) * (percentAlive/100) )
        for _ in range(numberToLive):
            row, column = cellLocations.pop()
            self.cells[row][column].live()



def test_world():
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
    for _ in range(500):
        w.better_populate_cells(25)
        print(w)



if __name__ == '__main__':
    test_world()