#----Player----#
class Player:
    """
    Player class to add player's score and get player's score
    """
    def __init__(self, name):
        """
        Player class to create a Player with given name.
        Initial score set to 0

        :param name: The name of the Player
        """
        self.name = name
        self.score = 0

    def add_score(self,score):
        """
        Add new score to the Player's current score.

        :param score: The new score to add. 
        """
        if score == None or score ==0:
            return f'{self.score}'
        else:
            print(score)
            self.score += score
            return f'{self.score}'

    def get_score(self):
        """
        :return: The Player's score.
        """
        return self.score
    def __str__(self):
        """
        :return : A String representation of the Player.
        """
        #string method to return players name and score
        return f'{self.name}: {self.score}'