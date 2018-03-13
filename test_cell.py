import unittest
from cell import Cell


class MyTestCase(unittest.TestCase):

    def test_create_living_and_dead_cells(self):
        row = 1
        column = 2
        cell = Cell(row, column)
        self.assertEqual(cell.alive, False)
        self.assertEqual(cell.row, row)
        self.assertEqual(cell.column, column)

    def test_live(self):
        cell = Cell(1,1)
        cell.live()
        self.assertTrue(cell.alive)

    def test_die(self):
        cell = Cell(1,1)
        cell.live()
        cell.die()
        self.assertFalse(cell.alive)

    def test_str(self):
        liveCell = Cell(1,1).live()
        deadCell = Cell(2,2).die()
        self.assertEqual(str(liveCell), '\u26AB')
        self.assertEqual(str(deadCell), '\u26AA')


if __name__ == '__main__':
    unittest.main()
