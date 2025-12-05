from django.shortcuts import render
from django.http import HttpResponse
import random
from .Board import board
from .models import Tile, Player
from django.shortcuts import redirect
from django.http import Http404

def home(request):
    players = Player.objects.all()
    context = {
        
        'players' : players 
    }

    return render(request, 'home.html', context=context)


def index(request):
    """
    Get all the Tile and Players objects and put them on the html file
    which renders all of them
    return: render the html file using request
    """
   
    Tiles = Tile.objects.all()
    players = Player.objects.all()

    context = {
        'Tiles' : Tiles ,
        'players' : players 
    }
  
    return render(request, 'template.html', context=context)


def check_player(request,name):
    """
    Get all the Tile and Players objects and put them on the html file
    which renders all of them
    return: render the html file using request
    """
    
    Tiles = Tile.objects.all()
    players = Player.objects.all()

    context = {
        'Tiles' : Tiles ,
        'players' : players 
    }
    if name == "One":
        return render(request, 'One.html', context=context)
    else:
        return render(request, 'Two.html', context=context)



def create_board( board_size):
    """
    First delete any old tile object
    create a board using create_Tile method from Tile class and save it
    return: Board created using all the tiles
    """

    Tile.objects.all().delete()

    for i in range(board_size):
        for j in range(board_size):
            Tile.create_Tile(i,j,'_','\u2610').save() 
    return Tile.objects.all().order_by('row','col')
    
def final(request):
    """
    First create a board of 10 using create_board function
    Then put treasure on the board using treasure function
    
    """
    Tiles = create_board(10)
    treasures()
    players = final2()
    context = {
        'Tiles' : Tiles ,
        'players' : players 
    }
    return render(request, 'template.html', context=context)

#create players
def final2():
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
    :param self: t , treasure
    :return: treasures on board
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
    board_size = 10
    all_tiles = '\u2610'
    blank_tiles = '\u2423'
    treasure_tiles = '\U0001F4B8'
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
            if tile.unicode_value == treasure_tiles: 
                tile.unicode_value = treasure_tiles
                tile.save()
            else:
                tile.unicode_value = blank_tiles
                tile.save()
            if name == "One":
                return redirect('/game/One/One')
            else:
                return redirect('/game/Two/Two') 
        else:
            player.score += int(tile.value)
            player.save()
            tile.save()
            
            tile.unicode_value = treasure_tiles
            tile.value = '_'
            tile.save()
            if name == "One":
                return redirect('/game/One/One')
            else:
                return redirect('/game/Two/Two') 
            
