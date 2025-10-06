import random


class board:

    """
    class to manage and create board and put treasure on it which moves according to
    the conditions
    """

#kind of contructor in which n is the box size and t is the treasure
    def __init__(self,n,t):
        self.n = n
        self.t = t
        self.score = 0
        #created a board variable to use using the function create board
        self.board = self.createBoard()

#string reperesentatiion of the class
    def __str__(self):
        boardArray =  [['_' for i in range(self.n)]for i in range(self.n)]

        return boardArray

#create a board
    def createBoard(self):
        try:
            boardArray = [['_' for i in range(self.n)]for i in range(self.n)]

            if self.n < 0:
                raise ValueError("Need a positive Integer")
        except ValueError as details:
            print(str(details))
        else:
            return boardArray


    def printboard(self):
        # for loop for printing board elements not array
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[i][j], end=' ')
            print()




    def moveUp(self,treasure,x,y):
        """
        this is for going vertical where y does not change
        and it move up after checking if there is _ or not
        :param treasure: the treasure
        :param x:the x-axis
        :param y:the y-axis
        :return:true or false if i should move or not
        """
        fixedNumberToCheck = y
        for i in range(treasure):
            fixedNumberToCheck = fixedNumberToCheck-1
            if self.board[fixedNumberToCheck][x] != '_':
                return False

        #put it back if there is same so it can move
        fixedNumberToCheck = y
        for i in range(treasure):
            #move up
            fixedNumberToCheck = fixedNumberToCheck -1
            #position for that treasure
            self.board[fixedNumberToCheck][x] = treasure
        return True

    def moveHorizontal(self, treasure, x, y):
        """
        this is for going horizontal where x does not change
        and it move after checking if there is _ or not
        :param treasure: the treasure
        :param x:the x-axis
        :param y:the y-axis
        :return:true or false if i should move or not
        """
        fixedNumberToCheck = x
        for i in range(treasure):
            fixedNumberToCheck = fixedNumberToCheck - 1
            if self.board[y][fixedNumberToCheck] != '_':
                return False

        # put it back if there is same so it can move
        fixedNumberToCheck = x
        for i in range(treasure):
            # move up
            fixedNumberToCheck = fixedNumberToCheck - 1
            # position for that treasure
            self.board[y][fixedNumberToCheck] = treasure
        return True

    def treasures(self):

        """
        generate random treasures from t to 1 on the board at positions horizontanl or vertical
        then check at every step if t = number of treasures on board. whenever treasure is on board
        make sure to check if its not coliding with other treasures
        :param self: t , treasure
        :return: treasures on board
        """
        count = 0
        treasure = self.t
        while (count < self.t):
            # get x and y for treasure like x = (0,9) and y = (0,9)  if n = 10
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)

            #random(0,1) == (0,y)
            if random.randint(0,1) == 0:
                if self.moveUp(treasure,x,y):
                    treasure = treasure -1
                    count += 1
            else:#random(1,0) == (x,0)
                if self.moveHorizontal(treasure,x,y):
                    treasure = treasure -1
                    count += 1


    def pick(self, row, column):

        try:
            if row < 0 or row >= self.n or column < 0 or column >= self.n:
                raise ValueError("Row and Column not in range")
            else:
                if  self.board[row][column] != '_':
                    val = self.board[row][column]
                    self.board[row][column] = '_'
                    self.score += val
                    return val
                else:
                    return 0

        except ValueError as details:
            print(str(details))

    def scores(self):
        return self.score

