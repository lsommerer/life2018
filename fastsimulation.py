from fastgeneration import FastGeneration
from simulation import Simulation
from menu import Menu
from toolbox import get_integer, get_string, get_boolean, is_integer
from time import sleep
from os import listdir, path, mkdir

class FastSimulation(Simulation):

    def __init__(self, rows=34, columns=72, percentAlive=50, geometry='dish'):
        self.initialPercentAlive = percentAlive
        self.geometry = geometry
        self.rules = [[2,3],[3]]
        self.generation = FastGeneration(rows, columns, self.geometry)
        self.generation.assign_neighbors()
        self.generation.populate_cells(percentAlive)
        self.mainMenu = Menu(Simulation.mainMenu)
        self.moreMenu = Menu(Simulation.moreMenu)
        self.generationCount = 0
        self.percentAlive = percentAlive
        self.name = 'untitled world'
        self.message = 'Welcome to LIFE!'

    def create_world(self, size=None):
        """
        Create, populate and dispaly a new world
        :param size: [optional] list of the rows and columns in the new world
        :return: None
        """
        if size == None:
            size = [self.generation.rows, self.generation.columns]
        self.generation = FastGeneration(size[0], size[1], self.geometry, self.rules)
        self.generation.assign_neighbors()
        self.generation.populate_cells(self.initialPercentAlive)
        self.message = 'a whole new world'
        self.name = 'untitled world'
        print(self)

    def change_population_rate(self, percentAlive=None):
        """
        Create a new world with the given percent of cells alive.
        :param percentAlive: [optiona] Number of living cells out of total cells.
        :return: None
        """
        if percentAlive == None:
            percentAlive = get_integer('What percent should be alive?')
        self.generation = FastGeneration(self.generation.rows, self.generation.columns, self.geometry, self.rules)
        self.generation.assign_neighbors()
        self.generation.populate_cells(percentAlive)
        self.initialPercentAlive = percentAlive
        self.message = 'world population changed'
        self.generationCount = 0
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
        self.generation = FastGeneration(rows, columns, self.geometry, self.rules)
        self.generation.assign_neighbors()
        self.generation.populate_cells(self.initialPercentAlive)
        self.message = 'world size changed'
        self.generationCount = 0
        print(self)

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
            self.generation = FastGeneration(rows, columns, self.geometry, self.rules)
            self.generation.assign_neighbors()
            for cell in self.generation.cells():
                if textGeneration[cell.row][cell.column] != FastGeneration.deadASCII:
                    cell.live()
            if self.geometry == 'dish':
                self.generation.assign_neighbors_torus()
            else:
                self.generation.assign_neighbors_dish()
            self.name = filename.split('.')[1].split('/')[2]
            self.message = f'opened {self.name}'
            self.generationCount = 0
            print(self)

def main():
    s = Simulation(34, 72) #115 238 on 4k monitor   84 156 on small screen 7pt font
    s.intro()
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