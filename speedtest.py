from simulation import Simulation
from generation import Generation
from fastgeneration import FastGeneration
from fastergeneration import FasterGeneration
#
# Run this from the console with 'python3 -m cProfile speedtest.py'
#
# Or use the professional version of PyCharm: right click below and choose profile 'speedtest'
#
# You could probably speed the whole thing up by using skip instead of next, but how is that fun.
#
def speed_test():
    rows = 32
    columns = 74
    population = 30
    times = 10
    geometry = 'torus'
    generationType = FasterGeneration #Generation | FastGeneration | FasterGeneration

    s = Simulation(rows, columns, population, geometry, generationType)
    s.delay = 0

    command = s.next
    #command = s.skip_forward

    for x in range(times):
        print(f'round: {x} of {times}')
        s.create_world()
        command(200)


if __name__ == '__main__':
    speed_test()