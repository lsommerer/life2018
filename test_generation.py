import unittest
from generation import Generation
from cell import Cell

class MyTestCase(unittest.TestCase):
    def test_create(self):
        rows = 2
        columns = 4
        g = Generation(rows, columns)
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
        self.assertEqual(len(g), rows * columns)


    def test_count_living(self):
        rows = 2
        columns = 4
        g = Generation(rows, columns)
        g._cells[0][0].live()
        self.assertEqual(g.count_living(), 1)

        g._cells[1][3].live()
        self.assertEqual(g.count_living(), 2)


    def test_better_populate(self):
        rows = 3
        columns = 5
        g = Generation(rows, columns)
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








if __name__ == '__main__':
    unittest.main()
