from generation import Generation
from time import sleep


class Simulation(object):

    delay = 0.1

    def __init__(self, rows=5, columns=5, percentAlive=50):
        self.generation = Generation(rows, columns)
        self.generation.populate_cells(percentAlive)

    def __str__(self):
        return str(self.generation)

    def run(self, times=10):
        for _ in range(times):
            print(self)
            self.generation = self.generation.next_generation()
            sleep(Simulation.delay)

    def main_event_loop(self):
        pass

    def get_command(prompt,valid):
        """
        Prompts the user for a command and returns it. Optionally,
        the user can also append a parameter after the command.
        """
        commands = {'f':'forward',
                    'n': 'new',
                    'o': 'open',
                    's': 'save',
                    'k': 'skip',
                    'p': 'population rate',
                    'i': 'world size',
                    'l': 'long l',
                    'q': 'quit'
                    }
        print()
        userString = input(prompt)
        if len(userString) == 0:
            command = 'forward'
            parameter = '1'
        else:
            valid = ''.join(commands.keys())
            while userString[0].lower() not in valid:
                prompt = 'Please enter one of these letters: '+valid+' '
                userString = input(prompt).lower()
            command = commands[userString[0]]
            parameter = userString[1:].strip()
            if parameter == '':
                parameter = None
        return command, parameter

def main():
    s = Simulation(28, 60)
    command = None
    while command != 'quit':
        command, parameter = s.get_command('[N]ew  [F]orward  s[K]ip  [P]opulation  s[I]ze  [L]ong L  [Q]uit')
        print(f'command: {command} parameter: {parameter}')
    #s.run(1000)

if __name__ == '__main__':
    main()