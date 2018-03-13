import unittest
from world import World

class MyTestCase(unittest.TestCase):
    def test_create(self):
        rows = 2
        columns = 4
        w = World(rows, columns)
        #
        # Is the world the correct size?
        #
        self.assertEqual(w.rows, rows)
        self.assertEqual(len(w.cells), rows)
        self.assertEqual(w.columns, columns)
        self.assertEqual(len(w.cells[0]), columns)
        #
        # Are all the cells correct?
        #
        for row in range(rows):
            for column in range(columns):
                self.assertFalse(w.cells[row][column].alive)
                self.assertEqual(w.cells[row][column].row, row)
                self.assertEqual(w.cells[row][column].column, column)

    def test_str(self):
        w = World(2, 4)
        l = w.cells[0][0].liveChar
        d = w.cells[0][0].deadChar
        #
        # all dead?
        #
        worldString = '\n'+d+d+d+d+'\n'+d+d+d+d
        self.assertEqual(str(w), worldString)
        #
        # some alive?
        #
        w.cells[0][0].live()
        w.cells[1][3].live()
        worldString = '\n'+l+d+d+d+'\n'+d+d+d+l
        self.assertEqual(str(w), worldString)
        #
        # all alive?
        #
        w.better_populate_cells(100)
        worldString = '\n'+l+l+l+l+'\n'+l+l+l+l
        self.assertEqual(str(w), worldString)

    def test_len(self):
        rows = 2
        columns = 4
        w = World(rows, columns)
        self.assertEqual(len(w), rows * columns)

    def count_living(self, world):
        living = 0
        for row in range(world.rows):
            for column in range(world.columns):
                if world.cells[row][column].alive:
                    living += 1
        return living


    def test_better_populate(self):
        rows = 3
        columns = 5
        w = World(rows, columns)
        #
        # Why would you populate with zero% alive?
        #
        w.better_populate_cells(0)
        self.assertEqual(self.count_living(w), 0)
        #
        # 50% alive
        #
        w.better_populate_cells(50)
        self.assertEqual(self.count_living(w), int(rows*columns/2))
        #
        # 100% alive
        #
        w.better_populate_cells(100)
        self.assertEqual(self.count_living(w), rows*columns)











if __name__ == '__main__':
    unittest.main()
