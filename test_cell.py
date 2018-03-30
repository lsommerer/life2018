import unittest
from unittest.mock import MagicMock
from cell import Cell
from generation import Generation


class MyTestCase(unittest.TestCase):

    def test_create_cell(self):
        row = 1
        column = 2
        cell = Cell(row, column)
        self.assertEqual(cell.alive, False)
        self.assertEqual(cell.row, row)
        self.assertEqual(cell.column, column)
        self.assertEqual(cell.neighbors, [])

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
        self.assertEqual(str(liveCell), Cell.liveChar)
        self.assertEqual(str(deadCell), Cell.deadChar)

    def test_living_neighbors(self):
        g = Generation(5, 5)
        g.assign_neighbors()

        cells = [[0, 1, 0, 0, 1],
                 [0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 1],
                 [0, 0, 1, 1, 1],
                 [1, 1, 1, 1, 1]]

        for row in range(5):
            for column in range(5):
                if cells[row][column] == 1:
                    g._cells[row][column].live()

        correctCount = [[1, 0, 2, 2, 1],
                        [2, 3, 5, 4, 4],
                        [1, 2, 5, 6, 4],
                        [3, 6, 7, 8, 5],
                        [1, 3, 4, 5, 3]]

        for cell in g.cells():
            self.assertEqual(cell.living_neighbors(),
                             correctCount[cell.row][cell.column],
                             f'cell[{row}][{column}] != {correctCount[row][column]}')

    def test_next_state(self):
        c = Cell(0,0)
        c.die()
        c.living_neighbors = MagicMock(side_effect=[0,1,2,3,4,5,6,7,8])
        correctResults = [False, False, False, True, False, False, False, False, False]
        for index, expectedResult in enumerate(correctResults):
            nextState = c.next_state()
            self.assertEqual(nextState, expectedResult,
                             f'dead with {index} neighbors returned {nextState}.')

        c.live()
        c.living_neighbors = MagicMock(side_effect=[0,1,2,3,4,5,6,7,8])
        correctResults = [False, False, True, True, False, False, False, False, False]
        for index, expectedResult in enumerate(correctResults):
            nextState = c.next_state()
            self.assertEqual(nextState, expectedResult,
                             f'dead with {index} neighbors returned {nextState}.')



if __name__ == '__main__':
    unittest.main()
