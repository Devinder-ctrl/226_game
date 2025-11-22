from django.db import models

#Tile model for the board
class Tile(models.Model):
    #row and column of the tile
    row = models.IntegerField() 
    col = models.IntegerField()
    #value stored in the tile
    value = models.CharField(max_length=10)

    def __str__(self):
        """
        String representation of the tile object.
        """
        return f'({self.row},{self.col}) - {self.value}'
    @classmethod
    def create_Tile(cls, row, col, value):
        """
        Class method for creating tiles 
        """
        model = cls(row=row, col=col, value=value)
        model.full_clean() 
        return model
        
#model for player in the game
class Player(models.Model):
    #player's name and score
    name = models.CharField(max_length=10)
    score = models.IntegerField()

    def __str__ (self):
        """
        String representation of the player object.
        """
        return f'{self.name , self.score}'
        
    @classmethod
    def create_player(cls,name,score):
        """
        Class method for creating tiles 
        """
        model = cls(name=name, score = score)
        model.full_clean()
        return model
