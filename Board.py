import random
from Player import Player

#---------Board----------#
class board:

    """
    Class to manage and create board
    Put treasure on board and keep track of them
    Remove treasure from board and assign it to player's score

    """


    def __init__(self,n,t):
        """
        initialize n(board range), t(treasures),and score to 0 
        initialize board variable for create_board() function
        :param n: board range
        :param t: treasures number
        """
        
        self.n = n
        self.t = t
        self.score = 0
        self.board = self.create_board()

    def __str__(self):
        """
        Returns a string representation of the board.
        Each row is joined into a string, and rows are separated by newlines.
        """
        board_string = ""
        for i in self.board:
            board_string += "_".join(str(j) for j in i) + "\n"
        return board_string


#create a board
    def create_board(self):
        #check if board range is greater than 2, if its not throw value error else return board array
        if self.n < 2:
            raise ValueError("n must be greater than 2")

        else:
            board_array = [['_' for i in range(self.n)] for i in range(self.n)]
            return board_array


    def print_board(self):
        # for loop for printing board elements
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[i][j], end=' ')
            print()




    def move_up(self,treasure,x,y):
        """
        this is for going vertical where y does not change
        and it move up after checking if there is _ or not
        :param treasure: the treasure
        :param x:the x-axis
        :param y:the y-axis
        :return:true or false if i should move or not
        """
        fixed_number_to_check = y
        for i in range(treasure):
            fixed_number_to_check = fixed_number_to_check - 1
            if self.board[fixed_number_to_check][x] != '_':
                return False

        #put it back if its same, so it can move
        fixed_number_to_check = y
        for i in range(treasure):
            #move up
            fixed_number_to_check = fixed_number_to_check - 1
            #position for that treasure
            self.board[fixed_number_to_check][x] = treasure
        return True

    def move_horizontal(self, treasure, x, y):
        """
        this is for going horizontal where x does not change
        and it move after checking if there is _ or not
        :param treasure: the treasure
        :param x:the x-axis
        :param y:the y-axis
        :return:true or false if i should move or not
        """
        fixed_number_to_check = x
        for i in range(treasure):
            fixed_number_to_check = fixed_number_to_check - 1
            if self.board[y][fixed_number_to_check] != '_':
                return False

        # put it back if its, same so it can move
        fixed_number_to_check = x
        for i in range(treasure):
            # move up
            fixed_number_to_check = fixed_number_to_check - 1
            # position for that treasure
            self.board[y][fixed_number_to_check] = treasure
        return True

    def treasures(self):

        """
        generate random treasures from t to 1 on the board at positions horizontanl or vertical
        then check at every step if t = number of treasures on board. Whenever, treasure is on board
        make sure to check if its not coliding with other treasures
        :param self: t , treasure
        :return: treasures on board
        """
        count = 0
        treasure = self.t
        try:
            #validate treasure's range
            if self.t <= 0 or self.t > self.n:
                raise ValueError("treasure must be between n and 0")
            else:
                while (count < self.t):
                    # get x and y for treasure like x = (0,9) and y = (0,9)  if n = 10
                    x = random.randint(0, self.n - 1)
                    y = random.randint(0, self.n - 1)

                    #random(0,1) == (0,y)
                    if random.randint(0,1) == 0:
                        if self.move_up(treasure,x,y):
                            treasure = treasure -1
                            count += 1
                    else:#random(1,0) == (x,0)
                        if self.move_horizontal(treasure,x,y):
                            treasure = treasure -1
                            count += 1
        except ValueError as details:
            print(str(details))
            raise

    def pick(self, row, column):

        try:
            #validate row and column range
            if row < 0 or row >= self.n or column < 0 or column >= self.n:
                raise ValueError("Row and Column not in range")
            else:
                #if board is not _ then , score becomes equal to that position's treasure 
                #then set it _ , to make it empty
                if  self.board[row][column] != '_':
                    score = self.board[row][column]
                    self.board[row][column] = '_'
                    return score
                else:
                    return 0

        except ValueError as details:
            print(str(details))
            raise


