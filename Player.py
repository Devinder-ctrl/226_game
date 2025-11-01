#----Player----#
class Player:
    """
    Player class to add player's score and get player's score
    """
    def __init__(self, name):
        #initialize name and score to 0
        self.name = name
        self.score = 0

    def add_score(self,score):
        #if score is none then return score else add that score to old scores and return it  
        if(score == None):
            return f'{self.score}'
        else:
            self.score += score
            return f'{self.score}'

    def get_score(self):
        #get Player's score
        return self.score
    def __str__(self):
        #string method to return players name and score
        return f'{self.name}: {self.score}'