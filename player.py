"""
Provides a class for information to be stored about players
"""

from placement import Placement
import math

IGNOREGAMES = False
# The elo requirement for a win to be good/bad
NOTABLEELO = -80


class Player():
    """
    Represent a player who participated in challonge tournaments.

    Stores information such as name, elo, games played, etc.

    Fields include:
    name            str
    elo             int
    won             int
    played          int
    winnings        float
    placings        list of Placement objects
    h2hwins         dict
                    key: player object
                    value: list of match json objects
    h2hlosses       dict
                    key: player object
                    value: list of match json objects
    """

    # Starting elo for players
    DEFAULT_ELO = 1200

    def __init__(self, name):
        """
        Constructor method

        Args:
            name (str): Name of the player
            elo (int): Elo of the player
            won (int): Number of games won
            played (int): Number of games played
        """
        self.name = name
        self.elo = float(Player.DEFAULT_ELO)
        self.won = 0
        self.played = 0
        self.winnings = 0
        self.placings = []
        # Dictionary, keys are Player objects,
        # values are lists of Match json objects
        self.h2hwins = {}
        self.h2hlosses = {}

    def calculateWin(self, loser, match):
        """
        Calculate and apply a change in elo based on a win

        Args:
            loser (Player): Player that lost the game
        """
        #k = 64 * (self.won/self.played)
        R1 = 10**(self.elo/400)
        R2 = 10**(loser.elo/400)
        E1 = R1/(R1+R2)
        result = 1
        if match["scores-csv"] != None:
            score = match["scores-csv"]
        else:
            score = "1-0"
        if not IGNOREGAMES:
            if score in ["2-0", "3-1", "1-0", "0-1", "1-3", "0-2"]:
                result = 1
            elif score in ["2-1", "3-2", "1-2", "2-3"]:
                result = .8
            elif score in ["3-0", "0-3"]:
                result = 1.25
            else:
                return
        elif score not in ["2-0", "3-1", "1-0", "2-1", "3-2", "3-0", "0-2", \
                         "1-3", "0-1", "1-2", "2-3", "0-3"]:
            return
        self.played += 1
        self.won += 1
        self.elo = self.elo + self.kconst()*(result-E1)
        if loser not in self.h2hwins:
            self.h2hwins[loser] = []
        self.h2hwins[loser].append(match)

    def calculateLoss(self, winner, match):
        """
        Calculate and apply a change in elo based on a loss

        Args:
            winner (Player): Player that won the game
        """
        #k = 64 *((self.played-self.won)/self.played)
        R1 = 10**(winner.elo/400)
        R2 = 10**(self.elo/400)
        E2 = R2/(R1+R2)
        result = 0
        if match["scores-csv"] != None:
            score = match["scores-csv"]
        else:
            score = "1-0"
        if not IGNOREGAMES:
            if score in ["2-0", "3-1", "1-0", "0-1", "1-3", "0-2"]:
                result = 0
            elif score in ["2-1", "3-2", "1-2", "2-3"]:
                result = .2
            elif score in ["3-0", "0-3"]:
                result = -0.25
            else:
                return
        elif score not in ["2-0", "3-1", "1-0", "2-1", "3-2", "3-0", "0-2", \
                         "1-3", "0-1", "1-2", "2-3", "0-3"]:
            return
        self.played += 1
        self.elo = self.elo + self.kconst()*(result-E2)
        if winner not in self.h2hlosses:
            self.h2hlosses[winner] = []
        self.h2hlosses[winner].append(match)

    def __str__(self):
        """
        Return a text representation of the player

        Returns:
            str: Formatted player stats
        """
        average = 0
        for placing in self.placings:
            average += placing.placement
        if len(self.placings) > 0:
            average = average/len(self.placings)
        if self.played == 0:
            playedtemp = 1
        else:
            playedtemp = self.played
        return ("{:20s}".format(self.name) + \
                " " + "{:0>4.0f}".format(self.elo) + \
                " " + "{:>4d}".format(self.won) + \
                " " + "{:>4d}".format(self.played) + \
                "   " + "{:0>4.3f}".format(self.won/playedtemp) + \
                "   " + "{:>4.3f}".format(average)
                )

    def record_tourney(self, tournament, player):
        """
        Record the results from a tournament.

        Needs the tournament json object and the player json object.
        Player json object needs to be from the same tournament.
        """
        self.placings.append(Placement(self.name, tournament, player))

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
                # Displays date and game count
                string += str(match["started-at"])[0:10] + ": " \
                          + str(match["scores-csv"])
                string += "\n"
        string += "Losses:\n"
        if other_player in self.h2hlosses:
            for match in self.h2hlosses[other_player]:
                # Displays date and game count
                string += str(match["started-at"])[0:10] + ": " \
                          + str(match["scores-csv"])
                string += "\n"
        return string

    def summary(self):
        """
        Return a string summarizing the player, including
        placings, notable wins, and notable losses.

        Returns:
            str: Summary of player
        """
        # Player name
        string = "Player: " + self.name + "\n"
        # Placings
        string += "Placings:\n"
        for placing in self.placings:
            string += "\t" + str(placing) + "\n"
        # Notable wins
        string += "Notable wins:  "
        for player in self.h2hwins:
            if player.elo >= self.elo + NOTABLEELO:
                string += player.name + ", "
        string = string[:-2] + "\n"
        # Notable losses
        string += "Notable losses:  "
        for player in self.h2hlosses:
            if player.elo <= self.elo + NOTABLEELO:
                string += player.name + ", "
        string = string[:-2] + "\n"
        return string

    def kconst(self):
        """
        Return the value of the constant k for elo calculation.

        Returns:
            int: Value of constant to use to calculate elo
        """
        return 32
        elodiff = abs(Player.DEFAULT_ELO - self.elo)
        variance = math.sqrt(elodiff) * 1.5
        return int(48 - variance)
        if self.elo <= 1200:
            return 60
        if self.elo <= 1300:
            return 40
        if self.elo <= 1400:
            return 30
        if self.elo <= 1500:
            return 20
        return 10
        #return 96/math.sqrt(self.played)

    __repr__ = __str__

