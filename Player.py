from Treasure import Treasure
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0



    def get_score(self):
        return f'{self.score}'
    def __str__(self):
        return f'{self.name}: {self.score}'