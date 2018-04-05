from generation import Generation
from fastgeneration import FastGeneration
from fastergeneration import FasterGeneration
from menu import Menu
from toolbox import get_integer, get_string, get_boolean, get_integer_between
from time import sleep
from os import listdir, path, mkdir

class Simulation(object):

    delayList = [5, 3, 2, 1.5, 1, 0.75, 0.5, 0.25, 0.1, 0.05, 0]
    defaultDirectory = './worlds/'
    libraryDirectory = './library/'

    mainMenu = [['create',      '[C]reate',    'Cc',   'integer2', False],
                ['next',        '[N]ext',      'Nn',   'integer1', True],
                ['skip',        's[K]ip',      'Kk',   'integer1', False],
                ['previous',    'pr[E]vious',  'Ee',   'integer1', False],
                ['skip back',   'skip [B]ack', 'Bb',   'integer1', False],
                ['save',        '[S]ave',      'Ss',   'string1',  False],
                ['open',        '[O]pen',      'Oo',   'string1',  False],
                ['library',     '[L]ibrary',   'Ll',   'string1',  False],
                ['more',        '[M]ore',      'Mm',   'string1',  False],
                ['help',        '[H]elp',      'Hh?',   None,      False],
                ['quit',        '[Q]uit',      'Qq',    None,      False],
                ['population',  '',            'Pp',   'integer1', False],
                ['geometry',    '',            'Gg',    None,      False],
                ['rule change', '',            'Rr',   'integer2', False],
                ['size',        '',            'Ii',   'integer2', False]]

    moreMenu = [['population',  '[P]opulaion', 'Pp',   'integer1', False],
                ['size',        's[I]ze',      'Ii',   'integer2', False],
                ['geometry',    '[G]eometry',  'Gg',    None,      False],
                ['rule change', '[R]ules',     'Rr',   'integer2',  False],
                ['speed',       '[S]peed',     'Ss',   'integer1',  False],
                ['more help',   '[H]elp',      'Hh?',   None,      False],
                ['back',        '[B]ack',      'Bb',    None,      True]]


    def __init__(self, rows=34, columns=72, percentAlive=50, geometry='dish', generationType=FasterGeneration):
        """

        :rtype: object
        """
        self.initialPercentAlive = percentAlive
        self.geometry = geometry
        self.rules = [[2,3],[3]]
        self.generationType = generationType # Generation | FastGeneration | FasterGeneration
        self.generation = self.generationType(rows, columns, self.geometry)
        self.generation.assign_neighbors()
        self.generation.populate_cells(percentAlive)
        self.mainMenu = Menu(Simulation.mainMenu)
        self.moreMenu = Menu(Simulation.moreMenu)
        self.generationCount = 1
        self.percentAlive = percentAlive
        self.name = 'untitled world'
        self.message = 'Welcome to LIFE!'
        self.timeLine = []
        self.delay = Simulation.delayList[5]

    def __str__(self):
        return str(self.generation) + self.status_bar()

    def status_bar(self):
        bar = '\n'
        bar += f'world:{self.name}  '
        bar += f'rules: {self.rule_string()}  '
        bar += f'geometry:{self.geometry}  '
        bar += f'size:{self.generation.rows}x{self.generation.columns}  '
        bar += f'generations:{self.generationCount}  '
        bar += f'living:{int(self.generation.count_living()/len(self.generation)*100)}%  '
        if self.message:
            bar += f'    *{self.message}*'
        return bar

    def rule_string(self):
        ruleString = ''
        for rule in self.rules:
            if len(rule) == 1:
                more =  str(rule[0])
            else:
                more = ''.join([str(number) for number in rule])
            ruleString += more + '/'
        ruleString = ruleString[:-1] + ''
        return ruleString

    def intro(self):
        self.open('intro.life', './library')
        sleep(1)
        temp = self.delay
        self.delay = 1.6
        self.next(2)
        self.delay = 0.8
        self.next(4)
        self.delay = 0.4
        self.next(8)
        self.delay = 0.2
        self.next(24)
        sleep(1)
        self.delay = temp

    def run(self):
        """Main event loop for the simulation."""
        self.help('help.txt')
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
            elif command == 'previous':
                self.previous(parameter)
            elif command == 'skip back':
                self.skip_backwards(parameter)
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
            elif command == 'geometry':
                self.toggle_geometry()
            elif command == 'rule change':
                self.rule_change(parameter)
            elif command == 'more':
                self.more()
            elif command == 'help':
                self.help('help.txt')
            elif command == 'quit':
                print('goodbye.')
            else:
                raise TypeError(f"command:'{command}' parameter:'{parameter}' not supported.")

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
        elif command == 'back':
            print(self)
        elif command == 'population':
            self.change_population_rate(parameter)
        elif command == 'geometry':
            self.toggle_geometry()
        elif command == 'size':
            self.change_world_size(parameter)
        elif command == 'speed':
            self.change_speed(parameter)
        elif command == 'rule change':
            self.rule_change(parameter)
        else:
            raise TypeError(f"command:'{command}' parameter:'{parameter}' not supported.")

    def create_world(self, size=None):
        """
        Create, populate and dispaly a new world
        :param size: [optional] list of the rows and columns in the new world
        :return: None
        """
        if size == None:
            size = [self.generation.rows, self.generation.columns]
        self.generation = self.generationType(size[0], size[1], self.geometry, self.rules)
        self.generation.assign_neighbors()
        self.generation.populate_cells(self.initialPercentAlive)
        self.message = 'a whole new world'
        self.name = 'untitled world'
        self.generationCount = 1
        self.timeLine = []
        print(self)

    def is_stable(self):
        return self.generation.is_stable(self.timeLine)

    def next(self, generations=None):
        """
        Generate and display the next generation of cells.
        :param generations: [optional] number of generations to display.
        :return: None
        """
        if generations == None:
            generations = 1
        start = generations-1
        current = 0
        stable = False
        while (current < generations) and not stable:
            self.timeLine.append(self.generation.get_generation())
            self.generation = self.generation.next_generation()
            self.generationCount += 1
            self.message = f' left: {start - current} '
            print(self)
            sleep(self.delay)
            stable = self.is_stable()
            current += 1
        if stable:
            self.message = 'Reached a stable position'
        else:
            self.message = ''
        print(self)

    def previous(self, generations=None):
        """
        Pop the last generation off of the timeline if it is available and make it the
        current world.
        :param generations: [optional] How many generations to go back.
        :return:
        """
        if generations == None:
            generations = 1
        if generations > len(self.timeLine):
            generations = len(self.timeLine)
        start = generations - 1
        if generations:
            for current in range(generations):
                self.generation.set_generation(self.timeLine.pop())
                self.generationCount -= 1
                self.message = f' left: {start - current} '
                print(self)
                sleep(self.delay)
            self.message = ''
        else:
            self.message = 'No previous generations exist.'
            print(self)

    def skip_forward(self, generations=None):
        """
        Loop through the number of generations specified without displaying the
        intermediate generations.
        :param generations: [optional] number of generations to skip
        :return: None
        """
        if generations == None:
            generations = get_integer('How many generations?')
        stable = False
        current = 0
        while (current < generations) and not stable:
            self.timeLine.append(self.generation.get_generation())
            self.generation = self.generation.next_generation()
            current += 1
            stable = self.is_stable()
        self.message = f'skipped forward {current} '
        if stable:
            self.message += '[stable position reached]'
        self.generationCount += current
        print(self)

    def skip_backwards(self, generations=None):
        """
        Loop through the number of generations specified without displaying the
        intermediate generations.
        :param generations: [optional] number of generations to skip
        :return: None
        """
        if generations == None:
            generations = get_integer('How many generations?')
        if generations > len(self.timeLine):
            generations = len(self.timeLine)
        if generations:
            for _ in range(generations):
                self.generation.set_generation(self.timeLine.pop())
                self.generationCount -= 1
            self.message = f'skipped backwards {generations} generations'
        else:
            self.message = 'No previous generations exist.'
        print(self)

    def change_population_rate(self, percentAlive=None):
        """
        Create a new world with the given percent of cells alive.
        :param percentAlive: [optiona] Number of living cells out of total cells.
        :return: None
        """
        if percentAlive == None:
            percentAlive = get_integer('What percent should be alive?')
        self.generation = self.generationType(self.generation.rows, self.generation.columns, self.geometry, self.rules)
        self.generation.assign_neighbors()
        self.generation.populate_cells(percentAlive)
        self.initialPercentAlive = percentAlive
        self.message = 'world population changed'
        self.generationCount = 1
        self.timeLine = []
        print(self)

    def change_speed(self, speed=None):
        """
        Create a new world with the given percent of cells alive.
        :param percentAlive: [optiona] Number of living cells out of total cells.
        :return: None
        """
        if (speed is None) or (speed not in [0,1,2,3,4,5,6,7,8,9,10]):
            speed = get_integer_between(0, 10, 'What speed?')
        self.delay = Simulation.delayList[speed]
        self.message = f'speed set to {speed}'
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
        self.generation = self.generationType(rows, columns, self.geometry, self.rules)
        self.generation.assign_neighbors()
        self.generation.populate_cells(self.initialPercentAlive)
        self.message = 'world size changed'
        self.generationCount = 1
        self.timeLine = []
        print(self)

    def rule_change(self, newRules=None):
        """
        Change the rules for the simulation.
        :param newRules: string with two integers separated by a space:
                         integer1: number of neighbors where a cell continues living
                         integer2: number of neighbors where a dead cell comes alive

                         The default rules are: '23 3'
        :return:
        """
        if newRules is None:
            self.help('rules.txt')
            remainAlive = get_integer('Cells remaing alive with this many neighbors:')
            generate =  get_integer('Cells become alive with this many neighbors :')
        else:
            remainAlive = newRules[0]
            generate = newRules[1]
        remainAlive = [int(number) for number in str(remainAlive)]
        generate = [int(number) for number in str(generate)]
        self.rules = [remainAlive, generate]
        self.generation.rules = self.rules
        self.message = 'The rules have changed'
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
        self.name = filename.split('.')[1].split('/')[2]
        self.message = f'saved {self.name}'
        print(self)

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
            self.message = '404 -No files found. Try saving one first.'
        else:
            myFile = open(filename, 'r')
            textGeneration = myFile.read()
            myFile.close()
            textGeneration = textGeneration.split('\n')[1:]
            rows = len(textGeneration)
            columns = len(textGeneration[0])
            self.generation = self.generationType(rows, columns, self.geometry, self.rules)
            self.generation.assign_neighbors()
            for cell in self.generation.cells():
                #
                # Having multiple types of Generations makes this annoyingly complicated. I should
                # really rewrite this so that each type of Generation has a procedure that turns
                # a cell in the row, column coordinates alive. That would let me replace the 10
                # lines with something like:
                #
                # if textGeneration[cell.row][cell.column] != self.generationType.deadASCII:
                #    self.generation.live(row, column)
                #
                if type(self.generation) is Generation:
                    if textGeneration[cell.row][cell.column] != self.generationType.deadASCII:
                        cell.live()
                elif type(self.generation) is FasterGeneration:
                    if textGeneration[cell[0]][cell[1]] != self.generationType.deadASCII:
                        self.generation.livingCells.append((cell[0],cell[1]))
                elif type(self.generation) is FastGeneration:
                    raise TypeError('FastGeneration open not implemented yet')
            if type(self.generation) is FasterGeneration:
                self.generation.livingCells = frozenset(self.generation.livingCells)
            #
            # Marking the end of the section that could be replaced by moving functionality into
            # the Generatin objects.
            #
            self.name = filename.split('.')[1].split('/')[2]
            self.message = f'opened {self.name}'
            self.generationCount = 1
            self.timeLine = []
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

    def toggle_geometry(self):
        if self.geometry == 'dish':
            self.geometry = 'torus'
            self.message = 'The world wraps around like a donut.'
        else:
            self.geometry = 'dish'
            self.message = 'The world ends at the edges.'
            self.generation.assign_neighbors()
        print(self)

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
    s = Simulation(34, 72) #115 238 on 4k monitor   84 156 on small screen 7pt font
    #s.intro()
    s.run()

def speed_test():
    s = Simulation(34, 72)
    s.delay = 0
    s.toggle_geometry()
    s.create_world()
    s.next(200)
    s.create_world()
    s.next(200)
    s.create_world()
    s.next(200)
    s.create_world()
    s.next(200)
    s.create_world()
    s.next(200)



if __name__ == '__main__':
    main()
    #speed_test()