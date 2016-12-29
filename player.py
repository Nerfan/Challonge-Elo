"""
Provides a class for information to be stored about players
"""
SEASON1 = False

class Player():

    def __init__(self, name, elo, won, played, winloss, winnings):
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
        self.winloss=winloss
        self.winnings = winnings

        # Dictionary, keys are Player objects,
        # values are lists of Match json objects
        self.h2hwins={}
        self.h2hlosses={}

    def calculateWin(self, loser, score="1-0"):
        """
        Calculate and apply a change in elo based on a win

        Args:
            loser (Player): Player that lost the game
        """
        self.played+=1
        self.won+=1
        self.winloss = (self.won/self.played)
        #k = 64 * (self.won/self.played)
        k = 32
        R1 = 10**(self.elo/400)
        R2 = 10**(loser.elo/400)
        E1 = R1/(R1+R2)
        result = 1.25
        if not SEASON1:
            if score in ["2-0", "3-1", "1-0", "0-1", "1-3", "0-2"]:
                result = 1.25
            elif score in ["2-1", "3-2", "1-2", "2-3"]:
                result = 1
            elif score in ["3-0", "0-3"]:
                result = 1.5
            else:
                return
        if score not in ["2-0", "3-1", "1-0", "2-1", "3-2", "3-0", "0-2", \
                         "1-3", "0-1", "1-2", "2-3,", "0-3"]:
            return
        self.elo=self.elo + k*(result-E1)

    def calculateLoss(self, winner, score="0-1"):
        """
        Calculate and apply a change in elo based on a loss

        Args:
            winner (Player): Player that won the game
        """
        self.played+=1
        self.winloss = (self.won/self.played)
        #k = 64 *((self.played-self.won)/self.played)
        k = 32
        R1 = 10**(winner.elo/400)
        R2 = 10**(self.elo/400)
        E2 = R2/(R1+R2)
        result = 0
        if not SEASON1:
            if score in ["2-0", "3-1", "1-0", "0-1", "1-3", "0-2"]:
                result = 0
            elif score in ["2-1", "3-2", "1-2", "2-3"]:
                result = .33
            elif score in ["3-0", "0-3"]:
                result = -0.25
            else:
                return
        if score not in ["2-0", "3-1", "1-0", "2-1", "3-2", "3-0", "0-2", \
                         "1-3", "0-1", "1-2", "2-3,", "0-3"]:
            return
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
                " " + "{:>4d}".format(self.played) + \
                "   " + "{:0>4.3f}".format(self.winloss) + \
                "   " + "{:>6.2f}".format(self.winnings))

    def wonTourney(self, entrants, place):
        """
        Adds to a players winnings based off their place, assumes 60/30/10 split
        and $2 game fee.
        :int param entrants: number of entrants in the tournament
        :int param place: 1/2/3 of the player.
        :return: None
        """
        if place == 1:
            self.winnings += ((entrants * 2) * .6)
        elif place == 2:
            self.winnings += ((entrants * 2) * .3)
        elif place == 3:
            self.winnings += ((entrants * 2) * .1)
        else:
            return

    def h2h_list(self):
        """
        Return a text representation of a players head-to-head records.

        Returns:
            str: Formatted player head-to-head stats
        """
        string = self.name + "'s head-to-head records:\n"
        for player in self.h2hwins:
            string += "{:20s}".format(player.name)
            string += ": " + str(len(self.h2hwins[player])) + "-"
            if player in self.h2hlosses:
                string += str(len(self.h2hlosses[player]))
            else:
                string += "0"
            string += "\n"
        for player in self.h2hlosses:
            if player not in self.h2hwins:
                string += "{:20s}".format(player.name)
                string += ": 0-" + str(len(self.h2hlosses[player]))
                string += "\n"
        return string

    def h2h_details(self, other_player):
        """
        Return a more detailed text representation of one head-to-head.

        Includes winner, date, and score.

        Args:
            other_player (Player): Player to compare head-to-head with

        Returns:
            str: Formatted details about a specific head-to-head
        """
        # Make sure we have data on the other player
        if not (other_player in self.h2hwins or other_player in self.h2hlosses):
            return "No matches against " + other_player.name + " recorded."
        string = self.name + "'s detailed head-to-head against " \
                 + other_player.name + ":\n"
        string += "Wins:\n"
        if other_player in self.h2hwins:
            for match in self.h2hwins[other_player]:
                string += str(match["started-at"])[0:10] + ": " \
                          + str(match["scores-csv"])
                string += "\n"
        string += "Losses:\n"
        if other_player in self.h2hlosses:
            for match in self.h2hlosses[other_player]:
                string += str(match["started-at"])[0:10] + ": " \
                          + str(match["scores-csv"])
                string += "\n"
        return string

    __repr__ = __str__
