#--------Test Player-------#
from Player import Player
def test_player():
    #check if player name equals to the given name and score is initialized to 0
    p = Player("TestPlayer")
    assert p.name == "TestPlayer"
    assert p.score == 0

    #check add score and get score functions
    p.add_score(10)
    assert p.get_score() == 10
    p.add_score(5)
    assert p.get_score() == 15

def test_add_score():
    p = Player("TestPlayer2")
    p.add_score(4)
    assert p.get_score() == 4
    p.add_score(None)
    assert p.get_score() == 4

def test_get_score():
    p = Player("TestPlayer2")
    p.add_score(10)
    assert p.get_score() == 10
    p.add_score(5)
    assert p.get_score() == 15

#---------Test Board---------#
import pytest
from Board import board

def test_str():
    b2 = board(4, 3)
    assert b2
# checking create board
def test_board():
    with pytest.raises(ValueError, match='n must be greater than 2'):
        b = board(1,2)

#check print board
def test_boardprint():
    b2 = board(4,3)
    b2.print_board()


# test moveUp in Board
def test_move_up():
    b2 = board(4, 3)

    b2.move_up(3, 2, 2)
    move = b2.move_up(3,2,2)
    assert move == False
    # assert b2.moveUp(3,1,5) == False # not possible 5 is out of range
    #possible


# test moveHorizontal in Board
def test_move_horizontal():
    move = True
    b2 = board(4, 3)

    b2.move_horizontal(3,1,2)
    move = b2.move_horizontal(3, 1, 2)
    assert move == False

   

#test treasures in board
def test_treasure():
    with pytest.raises(ValueError, match='treasure must be between n and 0'):
        b = board(4, -1)
        assert b.treasures()
    with pytest.raises(ValueError, match='treasure must be between n and 0'):
        b2 = board(4, 5)
        assert b2.treasures()

# test pick
def test_pick():
        b2 = board(4,3)
        b2.treasures()

        with pytest.raises(ValueError, match='Row and Column not in range'):
            b2.pick(4,4)
        with pytest.raises(ValueError, match='Row and Column not in range'):
            b2.pick(0, -4)

def test_pick2():


    score = 0
    b2 = board(4, 3)
    b2.treasures()
    for i in range(4):
        for j in range(4):
               score += b2.pick(i,j)
    assert score == 14





