class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self,score):
        if(score == None):
            return f'{self.score}'
        else:
            self.score += score
            return f'{self.score}'

    def get_score(self):
        return self.score
    def __str__(self):
        return f'{self.name}: {self.score}'