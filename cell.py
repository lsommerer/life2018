class Cell(object):

    def __init__(self, row, column):
        self._alive = False
        self.row = row
        self.column = column

    def __str__(self):
        if self._alive:
            return '\u26AB'
        else:
            return '\u26AA'

    def live(self):
        self._alive = True

    def die(self):
        self._alive = False


def test_cell():
    c = Cell(1,2)
    print(c)
    c.live()
    print(c)
    c.die()
    print(c)

if __name__ == '__main__':
    test_cell()