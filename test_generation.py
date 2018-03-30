import unittest
from generation import Generation
from cell import Cell

class MyTestCase(unittest.TestCase):
    def test_create(self):
        rows = 2
        columns = 4
        g = Generation(rows, columns)
        g.assign_neighbors()
        #
        # Is the world the correct size?
        #
        self.assertEqual(g.rows, rows)
        self.assertEqual(len(g._cells), rows)
        self.assertEqual(g.columns, columns)
        self.assertEqual(len(g._cells[0]), columns)
        #
        # Are all the cells correct?
        #
        for row in range(rows):
            for column in range(columns):
                self.assertFalse(g._cells[row][column].alive)
                self.assertEqual(g._cells[row][column].row, row)
                self.assertEqual(g._cells[row][column].column, column)

    def test_str(self):
        g = Generation(2, 4)
        g.assign_neighbors()
        l = Cell.liveChar
        d = Cell.deadChar
        #
        # all dead?
        #
        worldString = '\n'+d+d+d+d+'\n'+d+d+d+d
        self.assertEqual(str(g), worldString)
        #
        # some alive?
        #
        g._cells[0][0].live()
        g._cells[1][3].live()
        worldString = '\n'+l+d+d+d+'\n'+d+d+d+l
        self.assertEqual(str(g), worldString)
        #
        # all alive?
        #
        g.populate_cells(100)
        worldString = '\n'+l+l+l+l+'\n'+l+l+l+l
        self.assertEqual(str(g), worldString)

    def test_len(self):
        rows = 2
        columns = 4
        g = Generation(rows, columns)
        g.assign_neighbors()
        self.assertEqual(len(g), rows * columns)


    def test_count_living(self):
        rows = 2
        columns = 4
        g = Generation(rows, columns)
        g.assign_neighbors()
        g._cells[0][0].live()
        self.assertEqual(g.count_living(), 1)

        g._cells[1][3].live()
        self.assertEqual(g.count_living(), 2)


    def test_better_populate(self):
        rows = 3
        columns = 5
        g = Generation(rows, columns)
        g.assign_neighbors()
        #
        # Why would you populate with zero% alive?
        #
        g.populate_cells(0)
        self.assertEqual(g.count_living(), 0)
        #
        # 50% alive
        #
        g.populate_cells(50)
        self.assertEqual(g.count_living(), int(rows*columns/2))
        #
        # 100% alive
        #
        g.populate_cells(100)
        self.assertEqual(g.count_living(), rows*columns)


    def test_assign_neighbors(self):
        rows = 3
        columns = 3
        g = Generation(rows, columns)
        g.populate_cells()
        #
        # Do we have the correct number of neighbors?
        #
        correctNeighborCount = [3,5,3,
                                5,8,5,
                                3,5,3]
        for index, cell in enumerate(g.cells()):
            self.assertEqual(len(cell.neighbors), correctNeighborCount[index])
        #
        # Tediously test each cell
        #
        c = g._cells
        #
        #    x..
        #    ...
        #    ...
        #
        neighbors = c[0][0].neighbors
        correctNeighbors = [c[0][1], c[1][0], c[1][1]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[0][0]')
        #
        #    .x.
        #    ...
        #    ...
        #
        neighbors = c[0][1].neighbors
        correctNeighbors = [c[0][0], c[0][2], c[1][0], c[1][1], c[1][2]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[0][1]')
        #
        #    ..x
        #    ...
        #    ...
        #
        neighbors = c[0][2].neighbors
        correctNeighbors = [c[0][1], c[1][1], c[1][2]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[0][2]')
        #
        #    ...
        #    x..
        #    ...
        #
        neighbors = c[1][0].neighbors
        correctNeighbors = [c[0][0], c[0][1], c[1][1], c[2][0], c[2][1]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[1][0]')
        #
        #    ...
        #    .x.
        #    ...
        #
        neighbors = c[1][1].neighbors
        correctNeighbors = [c[0][0], c[0][1], c[0][2], c[1][0], c[1][2], c[2][0], c[2][1], c[2][2]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[1][1]')
        #
        #    ...
        #    ..x
        #    ...
        #
        neighbors = c[1][2].neighbors
        correctNeighbors = [c[0][1], c[0][2], c[1][1], c[2][1], c[2][2]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[1][2]')
        #
        #    ...
        #    ...
        #    x..
        #
        neighbors = c[2][0].neighbors
        correctNeighbors = [c[1][0], c[1][1], c[2][1]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[2][0]')
        #
        #    ...
        #    ...
        #    .x.
        #
        neighbors = c[2][1].neighbors
        correctNeighbors = [c[1][0], c[1][1], c[1][2], c[2][0], c[2][2]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[2][1]')
        #
        #    ...
        #    ...
        #    ..x
        #
        neighbors = c[2][2].neighbors
        correctNeighbors = [c[1][1], c[1][2], c[2][1]]
        self.assertEqual(set(neighbors), set(correctNeighbors), 'error at c[2][2]')


    def test_next_generation_blinker(self):
        l = Cell.liveChar
        d = Cell.deadChar
        n = '\n'
        state1 = n + d + l + d + \
                 n + d + l + d + \
                 n + d + l + d

        state2 = n + d + d + d + \
                 n + l + l + l + \
                 n + d + d + d

        g = Generation(3, 3)
        g.assign_neighbors()
        g._cells[0][1].live()
        g._cells[1][1].live()
        g._cells[2][1].live()

        self.assertEqual(state1, str(g))
        g = g.next_generation()
        self.assertEqual(state2, str(g))
        g = g.next_generation()
        self.assertEqual(state1, str(g))


    def test_next_generation_block(self):
        l = Cell.liveChar
        d = Cell.deadChar
        n = '\n'
        state1 = n + l + l + \
                 n + l + l

        g = Generation(2, 2)
        g.assign_neighbors()
        g._cells[0][0].live()
        g._cells[0][1].live()
        g._cells[1][0].live()
        g._cells[1][1].live()

        self.assertEqual(state1, str(g))
        g = g.next_generation()
        self.assertEqual(state1, str(g))
        g = g.next_generation()
        self.assertEqual(state1, str(g))


if __name__ == '__main__':
    unittest.main()
