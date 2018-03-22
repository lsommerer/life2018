from generation import Generation
from menu import Menu
from toolbox import get_integer
from time import sleep


class Simulation(object):

    delay = 0.1

    mainMenu = [['create',      '[C]reate',    'Cc',   'integer2', False],
                ['next',        '[N]ext',      'Nn',   'integer1', True],
                ['skip',        's[K]ip',      'Kk',   'integer1', False],
                ['population',  '[P]opulaion', 'Pp',   'integer1', False],
                ['size',        's[I]ze',      'Ii',   'integer2', False],
                ['long l',      '[L]ong L',    'Ll',   'integer2', False],
                ['help',        '[H]elp',      'Hh?',   None,      False],
                ['quit',        '[Q]uit',      'Qq',    None,      False]]


    def __init__(self, rows=5, columns=5, percentAlive=50):
        self.initialPercentAlive = percentAlive
        self.generation = Generation(rows, columns)
        self.generation.populate_cells(percentAlive)
        self.mainMenu = Menu(Simulation.mainMenu)

    def __str__(self):
        return str(self.generation)

    def run(self):
        """Main event loop for the simulation."""
        print(self)
        command = 'help'
        parameter = None
        while command != 'quit':
            if command == 'help':
                self.help()
            elif command == 'create':
                self.create_world(parameter)
            elif command == 'next':
                self.next(parameter)
            elif command == 'skip':
                self.skip_forward(parameter)
            elif command == 'population':
                self.change_population_rate(parameter)
            elif command == 'size':
                self.change_world_size(parameter)
            elif command == 'long l':
                self.create_long_l_world(parameter)
            if command != 'quit':
                self.mainMenu.display()
                command = self.mainMenu.command
                parameter = self.mainMenu.parameter

    def create_world(self, size=None):
        """
        Create, populate and dispaly a new world
        :param size: [optional] list of the rows and columns in the new world
        :return: None
        """
        if size == None:
            size = [self.generation.rows, self.generation.columns]
        self.generation = Generation(size[0], size[1])
        self.generation.populate_cells(self.initialPercentAlive)
        print(self)

    def next(self, generations=None):
        """
        Generate and display the next generation of cells.
        :param generations: [optional] number of generations to display.
        :return: None
        """
        if generations == None:
            generations = 1
        for _ in range(generations):
            self.generation = self.generation.next_generation()
            print(self)
            sleep(Simulation.delay)

    def skip_forward(self, generations=None):
        """
        Loop through the number of generations specified without displaying the
        intermediate generations.
        :param generations: [optional] number of generations to skip
        :return: None
        """
        if generations == None:
            generations = get_integer('How many generations?')
        for _ in range(generations):
            self.generation = self.generation.next_generation()
        print(self)

    def change_population_rate(self, percentAlive=None):
        """
        Create a new world with the given percent of cells alive.
        :param percentAlive: [optiona] Number of living cells out of total cells.
        :return: None
        """
        if percentAlive == None:
            percentAlive = get_integer('What percent should be alive?')
        self.generation.populate_cells(percentAlive)
        self.initialPercentAlive = percentAlive
        print(self)

    def change_world_size(self, size=None):
        """
        Create a new world with the given size.

        :param size: [optional] list containing the number of rows and columns
        :return: None
        """
        if size == None:
            rows = get_integer('How many rows should the new world have?')
            columns = get_integer('How many columns should the new world have?')
        else:
            rows = size[0]
            columns = size[1]
        self.generation = Generation(rows, columns)
        self.generation.populate_cells(self.initialPercentAlive)
        print(self)

    def create_long_l_world(self, size=None):
        """
        Create a world with cells living that look like a "long L"
        :param size: [optional] list containing the number of rows and columns
        :return: None
        """
        if size == None:
            size = [self.generation.rows, self.generation.columns]
        #
        # There is a minimum size for a Long L world.
        #
        if size[0] < 6: size[0] = 6
        if size[1] < 4: size[1] = 4
        self.generation = Generation(size[0], size[1])
        #
        # Start the Long L in roughly the center of the screen.
        #
        startRow = int(size[0]/2)-2
        startColumn = int(size[1]/2)-1
        #....
        #.O..
        #.O..
        #.O..
        #.OO.
        #....
        self.generation._cells[startRow][startColumn].live()
        self.generation._cells[startRow+1][startColumn].live()
        self.generation._cells[startRow+2][startColumn].live()
        self.generation._cells[startRow+3][startColumn].live()
        self.generation._cells[startRow+3][startColumn+1].live()
        print(self)


    def help(self):
        print('Help is on the way!')


def main():
    s = Simulation(32, 72)
    s.run()

if __name__ == '__main__':
    main()