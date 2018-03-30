from simulation import Simulation
from fastsimulation import FastSimulation
#
# Run this from the console with 'python3 -m cProfile speedtest.py'
#
# Or use the professional version of PyCharm: right click below and choose profile 'speedtest'
#
# You could probably speed the whole thing up by using skip instead of next, but how is that fun.
#
def speed_test():
    #s = FastSimulation(34, 72)
    s = Simulation(34, 72)
    s.delay = 0
    s.toggle_geometry()

    #command = s.next
    command = s.skip_forward

    times = 10
    for x in range(times):
        print(f'round: {x} of {times}')
        s.create_world()
        command(200)


if __name__ == '__main__':
    speed_test()