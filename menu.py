from toolbox import is_integer

class Menu(object):

    separator = '    '

    #
    # Positions in the menuItem list
    #
    command = 0
    displayAs = 1
    validLetters = 2
    parameterType = 3
    isDefault = 4

    def __init__(self, menuItems):
        """
        Expects menuItems in the form:

        menuItems = [[command, display, validLetters, parameterType, isDefault], ...]

        command: a string description of the command: 'help'
        display: what the menu displays for the command: '[H]elp'
        validLetters: the letters that resolve to this command: 'Hh?'
        parameterType: how any optional parameters are evaluated:
            'string1'
            'integer1'
            'integer2'
            None
        isDefault: True|False this item is selected if no items are selectd (return only)
        """

        self.menuItems = menuItems
        self.userInput = None
        self.command = None
        self.parameter = None

    def __str__(self):
        menuString = ''
        for menuItem in self.menuItems:
            menuString += menuItem[Menu.displayAs] + Menu.separator
        #
        # Take off the last Menu.separator
        #
        menuString = menuString[0:0-len(Menu.separator)]
        return menuString

    def valid(self, userInput):
        isValid = False
        userInput = userInput[0]
        for menuItem in self.menuItems:
            if userInput in menuItem[Menu.validLetters]:
                isValid = True
        return isValid

    def valid_letters(self):
        letters = ''
        for menuItem in self.menuItems:
            letters +=  menuItem[Menu.validLetters]
        return letters

    def default(self):
        """Returns the default menu option if one exists. Else, returns None"""
        defaultValue = None
        for menuItem in self.menuItems:
            if menuItem[Menu.isDefault]:
                defaultValue = menuItem[Menu.validLetters][0]
        return defaultValue

    def parse_command(self):
        command = None
        for menuItem in self.menuItems:
            if self.userInput[0] in menuItem[Menu.validLetters]:
                command =  menuItem[Menu.command]
        return command

    def parse_parameter(self):
        """Set the parameter if any."""
        #
        # Check what parameters this command takes
        #
        parameterType = None
        for menuItem in self.menuItems:
            if self.command == menuItem[Menu.command]:
                parameterType = menuItem[Menu.parameterType]

        parameter = None
        if parameterType == 'string1':
            parameter = self.userInput[1:].strip()
        elif parameterType == 'integer1':
            number = self.userInput[1:].strip()
            if is_integer(number):
                parameter = int(number)
        elif parameterType == 'integer2':
            numbers = self.userInput[1:].strip()
            if 'x' in numbers:
                numbers = numbers.split('x')
                if is_integer(numbers[0]) and is_integer(numbers[1]):
                    parameter = [int(numbers[0]), int(numbers[1])]
            elif ' ' in numbers:
                numbers = numbers.split(' ')
                if is_integer(numbers[0]) and is_integer(numbers[1]):
                    parameter = [int(numbers[0]), int(numbers[1])]
        return parameter

    def display(self):
        print(str(self)+'  ', end = '')
        userInput = input()
        #
        # The user might return the emply string.
        #
        if len(userInput) == 0:
            userInput = self.default()
        while (userInput == None) or (not self.valid(userInput[0])):
            userInput = input(f"please enter one of: '{self.valid_letters()}'")
            if len(userInput) == 0:
                userInput = self.default()
        self.userInput = userInput
        self.command = self.parse_command()
        self.parameter = self.parse_parameter()








