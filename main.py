from Board import board
from Player import Player
from Treasure import Treasure



#get board
b = board(4,4)
#get treasure on board
b.treasures()
#print board
b.printboard()

print()
#careating a player 'One'

while True :
    One = Player('1')
#prompt user to get row and column
    row = int(input('Enter a row'))
    column = int(input('Enter a column'))
#if there is treasure on those row and column then return the treasure value
    score = 0
    print(b.pick(row,column))

    b.printboard()
    print(b.scores())


