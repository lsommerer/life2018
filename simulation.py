from generation import Generation
from menu import Menu
from toolbox import get_integer, get_string, get_boolean
from time import sleep
from os import listdir, path, mkdir


class Simulation(object):

    delay = 0.1
    defaultDirectory = './worlds/'
    libraryDirectory = './library/'

    mainMenu = [['create',      '[C]reate',    'Cc',   'integer2', False],
                ['next',        '[N]ext',      'Nn',   'integer1', True],
                ['skip',        's[K]ip',      'Kk',   'integer1', False],
                ['save',        '[S]ave',      'Ss',   'string1',  False],
                ['open',        '[O]pen',      'Oo',   'string1',  False],
                ['library',     '[L]ibrary',   'Ll',   'string1',  False],
                ['more',        '[M]ore',      'Mm',   'string1',  False],
                ['help',        '[H]elp',      'Hh?',   None,      False],
                ['quit',        '[Q]uit',      'Qq',    None,      False],
                ['population',  '',            'Pp',   'integer1', False],
                ['size',        '',            'Ii',   'integer2', False]]

    moreMenu = [['population',  '[P]opulaion', 'Pp',   'integer1', False],
                ['size',        's[I]ze',      'Ii',   'integer2', False],
                ['more help',   '[H]elp',      'Hh?',   None,      False],
                ['back',        '[B]ack',      'Bb',    None,      True]]


    def __init__(self, rows=5, columns=5, percentAlive=50):
        self.initialPercentAlive = percentAlive
        self.generation = Generation(rows, columns)
        self.generation.populate_cells(percentAlive)
        self.mainMenu = Menu(Simulation.mainMenu)
        self.moreMenu = Menu(Simulation.moreMenu)

    def __str__(self):
        return str(self.generation)

    def intro(self):
        self.open('intro.life', './library')
        sleep(1)
        self.next(50)
        self.help('help.txt')

    def run(self):
        """Main event loop for the simulation."""
        command = 'do not quite the first time'
        while command != 'quit':
            self.mainMenu.display()
            command = self.mainMenu.command
            parameter = self.mainMenu.parameter
            if command == 'create':
                self.create_world(parameter)
            elif command == 'next':
                self.next(parameter)
            elif command == 'skip':
                self.skip_forward(parameter)
            elif command == 'save':
                self.save(parameter, Simulation.defaultDirectory)
            elif command == 'open':
                self.open(parameter, Simulation.defaultDirectory)
            elif command == 'library':
                self.open(parameter, Simulation.libraryDirectory)
            elif command == 'population':
                self.change_population_rate(parameter)
            elif command == 'size':
                self.change_world_size(parameter)
            elif command == 'more':
                self.more()
            elif command == 'help':
                self.help('help.txt')
            elif command == 'quit':
                print('goodbye.')
            else:
                raise TypeError(f'command: {command} parameter:{parameter} not supported.')


    def more(self):
        """
        Display the more menu and get a command and [optional] parameter from the user.
        :return: command, parameter
        """
        print(self)
        self.moreMenu.display()
        command = self.moreMenu.command
        parameter = self.moreMenu.parameter
        if command == 'more help':
            command, parameter = self.more_help()
        if command == 'back':
            print(self)
        if command == 'population':
            self.change_population_rate(parameter)
        if command == 'size':
            self.change_world_size(parameter)

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
        self.generation = Generation(self.generation.rows, self.generation.columns)
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

    def save(self, filename='', myPath='./'):
        """
        Save the current generation of the current world as a text file.
        :param filename: [optional] name of the file to save may already have '.life' at the end
        :param myPath: [optional] the directory to save the file in.
        :return: None
        """
        filename = self.get_filename_for_saving(filename, myPath)
        text = self.generation.as_text()
        myFile = open(filename, 'w')
        myFile.write(text)
        myFile.close()

    def get_filename_for_saving(self, filename, myPath='./'):
        """
        Make sure that the filename exists, that it has the right extension and that it goes into the
        correct directory.
        :param filename: name of the file, may be None at this point.
        :param myPath: Where the file should be saved.
        :return: The corrected filename with the path prepended.
        """
        if filename == '':
            filename = get_string('What do you want to call the file? ')
        #
        # Make sure the file has the correct file extension.
        #
        if filename[-5:] != '.life':
            filename = filename + '.life'
        #
        # Check if the file already exists.
        #
        if not path.isdir(myPath):
            mkdir(myPath)
        if filename in listdir(myPath):
            prompt = f"A file named '{filename}' already exists! Do you want to replace it?"
            replaceFile = get_boolean(prompt)
            if not replaceFile:
                filename = self.get_filename_for_saving('')
        #
        # Add on the correct path for saving files.
        #
        if filename[0:len(myPath)] != myPath:
            filename = path.join(myPath, filename)
        return filename

    def open(self, filename='', myPath='./'):
        """
        Open a previously saved world.
        :param filename: Name of the file to open
        :param path: Where to find the world files
        :return: None (changes the generation)
        """
        filename = self.get_filename_for_opening(filename, myPath)
        #
        # get_filename_for_opening return '' if there are no files available
        #
        if filename == '':
            print('404 -No files found. Try saving one first.')
        else:
            myFile = open(filename, 'r')
            textGeneration = myFile.read()
            myFile.close()
            textGeneration = textGeneration.split('\n')[1:]
            rows = len(textGeneration)
            columns = len(textGeneration[0])
            self.generation = Generation(rows, columns)
            for cell in self.generation.cells():
                if textGeneration[cell.row][cell.column] != Generation.deadASCII:
                    cell.live()
            print(self)

    def get_filename_for_opening(self, filename, myPath='./'):
        """Make sure the filename has the right extension, goes in
           the right directory and, if no name is given, provides a
           list of worlds."""
        #
        # Find the files that are available.
        #
        filesAvailable = False
        files = listdir(myPath)
        availableFiles = 'Available files: '
        for file in files:
            splitFile = file.split('.')
            if splitFile[-1] == 'life':
                availableFiles += splitFile[0] + ', '
                filesAvailable = True
        availableFiles = availableFiles[:-2]
        if filesAvailable:
            #
            # Make sure the file has the correct file extension.
            #
            if filename[-5:] != '.life':
                filename = filename + '.life'
            while filename not in files:
                print(availableFiles)
                filename = get_string('Which file do you want to open?')
                if filename[-5:] != '.life':
                    filename = filename + '.life'
                if filename not in files:
                    print('404: File not found...')

            #
            # Add on the correct path for saving files.
            #
            if filename[0:9] != myPath:
                filename = path.join(myPath, filename)
        else:
            filename = ''
        return filename

    def help(self, filename):
        """prints instructions on the screen"""
        file = open(filename, 'r')
        instructions = file.read()
        file.close()
        print(instructions)

    def more_help(self):
        self.help('morehelp.txt')
        self.moreMenu.display()
        command = self.moreMenu.command
        parameter = self.moreMenu.parameter
        return command, parameter


def main():
    s = Simulation(34, 72) #115 238 on 4k monitor
    s.intro()
    s.run()

if __name__ == '__main__':
    main()