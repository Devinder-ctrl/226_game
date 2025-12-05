from django.db import models


class Tile(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.CharField(max_length=10)
    unicode_value = models.CharField(max_length=10, default='\u2610')
    def __str__(self):
        return f'({self.row},{self.col}) - {self.value}'
    @classmethod
    def create_Tile(cls
    , row, col, value, unicode_value):
        model = cls(row=row, col=col, value=value, unicode_value=unicode_value)
        model.full_clean()
        return model
    class Meta:
        ordering = ('row','col')
# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=10)
    score = models.IntegerField()
    def __str__ (self):
        return f'{self.name , self.score}'
        
    @classmethod
    def create_player(cls,name,score):
        model = cls(name=name, score = score)
        model.full_clean()
        return model
