import sys


class GridPos:
    '''

    Creates a position object that will be used for the larger
    game.

    '''
    def __init__(self, x, y):
        '''

        Initializes the x and y positions of the point. Also,
        indicates if the position is occupied by a ship and
        if the point has been previously guessed.

        :param x: x-coordinate
        :param y: y-coordinate
        '''
        self._x = x
        self._y = y
        self._occupation = None
        self._guess = False

    def occupies(self, ship):
        '''

        Defines the ship occupying this position on the grid.

        :param ship:
        :return:
        '''
        self._occupation = ship

    def checkmark(self):
        '''

        If the position is checked, guess will become true.

        :return:
        '''
        self._guess = True

    def __str__(self):
        return "Grid Position at {:d}, {:d}".format(self._x, self._y)


class Board:
    def __init__(self):
        '''

        Initializes attributes for the entire grid and the ships
        that are on it.

        '''
        self._list = []
        self._collection = []

    def create(self):
        '''

        Creates the 10 x 10 grid.

        '''
        for i in range(11):
            for j in range(11):
                blank = GridPos(i, j)
                self._list.append(blank)

    def guess(self, x, y):
        '''

        Using x and y, program checks if these coordinates
        correspond to a ship's location.

        :param x: x-coordinate
        :param y: y-coordinate
        :return: True or False
        '''
        for i in self._list:
            if i._x == int(x) and i._y == int(y):
                if i._occupation != None:
                    i._occupation.hit(x, y)
                    if len(i._occupation._positions) == 0:
                        print("{} sunk".format
                              (i._occupation._type))
                        return 1
                    elif i._guess == False:
                        print('hit')
                        i.checkmark()
                    else:
                        print('hit (again)')
                    return 0
                else:
                    if i._guess == False:
                        print('miss')
                        i.checkmark()
                        return 0
                    else:
                        print('miss (again)')
                        return 0


    def ships(self, object, list):
        '''

        Adds ships to the positions they are desired in.

        :param object: a ship
        '''
        for i in object._positions:
            for grid in self._list:
                if grid._x == i._x and grid._y == i._y:
                    if grid._occupation != None:
                        empty = ''
                        for i in list:
                            empty += str(i) + ' '
                        print("ERROR: overlapping ship: "
                              + empty)
                        sys.exit()
                    grid.occupies(object)
                    break
        self._collection.append(object)


    def __str__(self):
        return "This is the Battleship board.".format()


class Ship:
    '''

    Creates a type of ship to be placed on the board.

    '''
    def __init__(self, what, size, line):
        '''

        Initializes the ship's type, line, size, and
        positions.

        :param what: the type of ship
        :param size: the size of the ship
        :param line: the line in the file
        '''
        self._type = what
        self._size = size
        self._line = line
        self._positions = []
        self._not_hit = []

    def placement(self, x, y):
        '''

        Places the ship at its corresponding points.

        :param x: x-coordinate
        :param y: y-coordinate
        '''
        blank = GridPos(x, y)
        self._positions.append(blank)
        self._not_hit.append(blank)

    def hit(self, x, y):
        '''

        If the ship is located on point (x,y), the ship is
        indicated as hit and no longer holds that position.

        :param x:
        :param y:
        :return:
        '''
        for i in self._positions:
            if int(x) == i._x and int(y) == i._y:
                self._not_hit.pop(self._positions.index(i))
                self._positions.pop(self._positions.
                                    index(i))

    def __str__(self):
        return "Ship: Type ~ {:d}, Size ~ {:d}".format\
            (self._type, self._size)


def main():
    placement = input('')
    guess = input('')
    game = Board()
    game.create()
    new_game = read_in(placement, game)
    part_two(guess, new_game)


def read_in(file, board):
    '''

    First the function reads in the placement file and
    then checks if the file follows the program's restrictions
    by using other functions in the program. Following that,
    each ship is created and placed to their desired positions
    on the board.

    :param file: the placement file
    :param board: the 10x10 grid
    :return: the edited 10x10 grid
    '''
    temporary = open(file, 'r')
    new = temporary.readlines()
    letters = ['A', 'B', 'S', 'D', 'P']
    ships = []
    for i in new:
        stripped = i.strip('\n')
        splitter = stripped.split()
        useful = []
        for j in splitter:
            useful.append(j)
        if useful[0] in letters:
            letters.pop(letters.index(useful[0]))
        else:
            print("ERROR: fleet composition incorrect")
            sys.exit(0)
        checks(useful)
        integers = [useful[0]]
        for string in range(1, len(useful), 1):
            integers.append(int(useful[string]))
        object = create(integers)
        ships.append(object)
    if len(ships) != 5:
        print("ERROR: fleet composition incorrect")
        sys.exit(0)
    for j in ships:
        board.ships(j, j._line)
    return board


def checks(list):
    '''

    Does a number of checks on each line of the file to
    verify if it follows the program's guidelines.

    :param list: the line of the file
    :return: nothing is returned if true, program ends if
    false
    '''
    for i in list[1:]:
        if int(i) > 10:
            empty = ''
            for i in list:
                empty += str(i) + ' '
            print("ERROR: ship out-of-bounds: " + empty)
            sys.exit(0)
    if list[2] != list[4] and list[1] != list[3]:
        empty = ''
        for i in list:
            empty += str(i) + ' '
        print("ERROR: ship not horizontal or vertical: "
              + empty)
        sys.exit(0)
    if size_check(list) != True:
        empty = ''
        for i in list:
            empty += str(i) + ' '
        print("ERROR: incorrect ship size: " + empty)
        sys.exit(0)


def size_check(list):
    '''

    Checks the size of the ship.

    :param list: the line of the file
    :return: if the size of the ship is allowed, true is
    returned, else false
    '''
    guide = {'A': 4, 'B': 3, 'S': 2, 'D': 2, 'P': 1}
    size = 0
    if list[1] == list[3]:
        temporary = int(list[4]) - int(list[2])
        actual = abs(temporary)
        size += actual
    elif list[2] == list[4]:
        temporary = int(list[3]) - int(list[1])
        actual = abs(temporary)
        size += actual
    if size == guide[list[0]]:
        return True
    else:
        return False


def create(list):
    '''

    Creates each ship and designates where they should be
    on the board.

    :param list: the line of the file
    :return: the ship object
    '''
    size = 0
    y = 0
    x = 0
    end = 0
    start = 0
    if list[1] == list[3]:
        temporary = list[4] - list[2]
        actual = abs(temporary)
        if list[4] > list[2]:
            start += list[2]    # From line 318 - 346
            end += list[4]      # file creates variables
            x += list[1]        # from where the ship
        else:                   # should start and end
            start += list[4]
            end += list[2]
            x += list[1]
        size += actual
    elif list[2] == list[4]:
        temporary = int(list[3]) - int(list[1])
        if list[3] > list[1]:
            start += list[1]
            end += list[3]
            y += list[2]
        else:
            start += list[3]
            end += list[1]
            y += list[2]
        actual = abs(temporary)
        size += actual
    ship = Ship(list[0], size, list)
    if x != 0:                  # Creates a ship and
        while start <= end:     # lists the grid
            ship.placement(x, start)
            start += 1          # points in the object
    else:
        while start <= end:
            ship.placement(start, y)
            start += 1
    return ship


def part_two(file, board):
    '''

    Reads in the guess file and processes each guess.
    Indication is given if each guess hits or misses the
    ships on the map. Program ends if either guess run
    out or all ships have sunk.

    :param file:
    :param board:
    :return:
    '''
    count = 0
    temporary = open(file, 'r')
    actual = temporary.readlines()
    for i in actual:
        stripped = i.strip('\n')
        splitter = stripped.split()
        if int(splitter[0]) >= 10:
            print("illegal guess")
        else:
            number = board.guess(splitter[0], splitter[1])
            count += number
        if count == 5:
            print('all ships sunk: game over')
            sys.exit(0)

main()
