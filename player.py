"""
Provides a class for information to be stored about players
"""

class Player():

    def __init__(self, name, elo, won, played):
        """
        Constructor method

        Args:
            name (str): Name of the player
            elo (int): Elo of the player
            won (int): Number of games won
            played (int): Number of games played
        """
        self.name=name
        self.elo=float(elo)
        self.won=won
        self.played=played

    def calculateWin(self, loser, score="1-0"):
        """
        Calculate and apply a change in elo based on a win

        Args:
            loser (Player): Player that lost the game
        """
        self.played+=1
        self.won+=1
        #k = 64 * (self.won/self.played)
        k = 32
        R1 = 10**(self.elo/400)
        R2 = 10**(loser.elo/400)
        E1 = R1/(R1+R2)
        result = 1
        if score == "2-0" or score == "3-1" or score == "1-0":
            result = 1 
        elif score == "2-1" or score == "3-2":
            result = .66
        elif score == "3-0":
            result = 1.25
        self.elo=self.elo + k*(result-E1)

    def calculateLoss(self, winner, score="1-0"):
        """
        Calculate and apply a change in elo based on a loss

        Args:
            winner (Player): Player that won the game
        """
        self.played+=1
        #k = 64 *((self.played-self.won)/self.played)
        k = 32
        R1 = 10**(winner.elo/400)
        R2 = 10**(self.elo/400)
        E2 = R2/(R1+R2)
        result = 0
        if score == "2-0" or score == "3-1" or score == "1-0":
            result = 0 
        elif score == "2-1" or score == "3-2":
            result = .33
        elif score == "3-0":
            result = -0.25
        self.elo=self.elo + k*(result-E2)

    def __str__(self):
        """
        Return a text representation of the player

        Returns:
            str: Formatted player stats
        """
        return ("{:20s}".format(self.name) + \
                " " + "{:0>4.0f}".format(self.elo) + \
                " " + "{:>4d}".format(self.won) + \
                " " + "{:>4d}".format(self.played))

    __repr__ = __str__
