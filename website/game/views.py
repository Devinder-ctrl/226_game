from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import random
from .Board import board
from .models import Tile, Player


def index(request):
    """
    Main page
    Get all the Tile and Players objects and put them on the html file
    which renders all of them
    
    """
    Tiles = Tile.objects.all()
    players = Player.objects.all()
    context = {
        'Tiles' : Tiles ,
        'players' : players 
    }
    return render(request, 'template.html', context=context)


def create_board( board_size):
    """
    create new board using given board size
    First delete any old tile object,
    create tiles using create_Tile method from Tile class and save it
    return: Board created using all the tiles
    """

    Tile.objects.all().delete()

    for i in range(board_size):
        for j in range(board_size):
            Tile.create_Tile(i,j,"_").save() 
    return Tile.objects.all()
    
def final(request):
    """
    First create a board of 10,
    Then place treasures on the board using 
    create two players
    render the board and players in the template

    """
    Tiles = create_board(10)
    treasures()
    players = create_all_players()

    context = {
        'Tiles' : Tiles ,
        'players' : players 
    }
    return render(request, 'template.html', context=context)

def create_all_players():
    """
    Create players
    first delete all the existing player objects
    Then create two players "One" and "Two" with score 0 
    Then save all players
    return: all player objects
    """
    Player.objects.all().delete()

    Player.create_player("One",0).save() 
    Player.create_player("Two",0).save() 
    
    return Player.objects.all()


def move_up(treasure,row,col):
    """
    this is for going vertical where y does not change
    and it move up after checking if there is _ or not
    :param treasure: the treasure
    :param x:the x-axis
    :param y:the y-axis
    :return:true or false if i should move or not
    """
    fixed = row
    if fixed - treasure < 0:
        return False
    for i in range(treasure):
        fixed -= 1
        tile = Tile.objects.get(row=fixed, col=col)
        if tile.value != '_':
            tile.value = '_'
            return False
    fixed = row
    for i in range(treasure):
        fixed = fixed - 1
        tile = Tile.objects.get(row=fixed, col=col)
        tile.value = str(treasure)
        tile.save()
    return True

def move_horizontal(treasure, row, col):
    """
    this is for going horizontal where x does not change
    and it move after checking if there is _ or not
    :param treasure: the treasure
    :param x:the x-axis
    :param y:the y-axis
    :return:true or false if i should move or not
    """
    fixed = col
    if fixed - treasure < 0:
        return False
    for i in range(treasure):
        fixed = fixed - 1
        tile = Tile.objects.get(row=row, col=fixed)

        if tile.value != "_":
            tile.value = '_'
            return False
    fixed = col
    for i in range(treasure):
        fixed = fixed - 1
        tile = Tile.objects.get(row=row, col=fixed)
        tile.value = str(treasure)
        tile.save()
        
    return True

def treasures():

    """
    generate random treasures from t to 1 on the board at positions horizontanl or vertical
    then check at every step if t = number of treasures on board. Whenever, treasure is on board
    make sure to check if its not coliding with other treasures
  
    """
   
    treasure = 4
    board_size = 10

    while treasure > 0:   

        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)

        if random.randint(0, 1) == 0:
            if move_up(treasure, row, col):
                treasure -= 1
             
        else:
            if move_horizontal(treasure, row, col):
                treasure -= 1
             

def pick(request, name, row, col):
    """
    Pick's a treasure from the board
    Check Player's name, row and column
    If tile contain a treasure, put it in that player's score
    set that tile to '_'
    redirect to game page 
    """
    board_size = 10
    if name != "One" and name != "Two":
        return HttpResponse("No Such Player")

    if row < 0 or row >= board_size or col < 0 or col >= board_size:
        return HttpResponse("Invalid row or column")
    else:
        #if board is not _ then , score becomes equal to that position's treasure 
        #then set it _ , to make it empty
        tile = Tile.objects.get(row=row, col=col)
        player = Player.objects.get(name=name)
        value = str(tile.value)
        
     
        if tile.value == '_': 
            return HttpResponse("No treasure found")
        else:
            player.score += int(tile.value)
            tile.value = '_'
            player.save()
            tile.save()
            return redirect('/game/')

