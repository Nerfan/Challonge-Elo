"""
Hold the list of elos and operate on it.

This class provides utilities to save and load the list, as well as edit it.
We have functions such as filtering and writing to a spreadsheet.
"""

import time
import xlsxwriter
import pickle
import os
import pathlib
import subprocess
import webbrowser
from elo_calculator import EloCalculator

SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))


class EloList:
    """
    Hold a list of Player objects and operate upon them.

    The Player objects contain information about elo and other ranking data.
    This class can filter, save, give a string representation of the list, etc.
    """

    """
    Fields:

    elolist: List of Player objects
    """

    def __init__(self):
        """
        Create a new instance of an EloList object.

        Takes no arguments, initializes the list to empty.
        """
        self.elolist = []

    def calculate_elos(self,
                       tournamentfile="obj/tournaments.pkl",
                       participantsfile="obj/participants.pkl",
                       matchesfile="obj/matches.pkl"):
        """
        Calculate changes to the list of elos based on saved tournaments.

        Args:
            tournamentfile (str): path to file of list of tournaments
            participantfile (str): path to file of list of participants
            matchfile (str): path to file of list of matches

            All of these files should have been created by save_tourneys.py
        """
        calculator = EloCalculator()
        calculator.set_elo_list(self.elolist)
        calculator.calculate(tournamentfile, participantsfile, matchesfile)
        self.elolist = calculator.get_elo_list()

    def export_spreadsheet(self):
        """
        Export a matchup chart of the players.

        Write directly to a file named "MU Chart.xlsx."

        Args:
            players:    list of Player objects
        """
        wbpath = os.path.join(SCRIPTDIR, "output", "MU Chart.xlsx")
        # Create the directory if it doesn't exist already
        dirpath = pathlib.Path(os.path.dirname(wbpath))
        dirpath.mkdir(parents=True, exist_ok=True)
        # Create the workbook
        workbook = xlsxwriter.Workbook(wbpath)
        worksheet = workbook.add_worksheet()
        # Create an array for easy access to ratios, this will be changed later
        # to be in-line
        sortedPlayers = sorted(list(self.elolist),
                               key=lambda x: x.elo, reverse=True)
        # Dictionary, keys are names
        #   Values are dictionaries, in which keys are opponent names
        #       Values are tuples of (win, loss)
        # i.e. h2h[player_name][opponent_name] = (wins, losses)
        h2h = {}
        # Loop through all players
        numplayers = 0
        for player in sortedPlayers:
            ratios = {}
            # Loop through each individual player's head-to-head records
            for opponent in sortedPlayers:
                if opponent in player.h2hwins:
                    wins = len(player.h2hwins[opponent])
                else:
                    wins = 0
                if opponent in player.h2hlosses:
                    losses = len(player.h2hlosses[opponent])
                else:
                    losses = 0
                ratios[opponent.name] = (wins, losses)
            numplayers += 1
            h2h[player.name] = ratios
        # Create color formats for the cells
        # TODO better gradients
        winning = workbook.add_format({"bg_color": "green"})
        losing = workbook.add_format({"bg_color": "red"})
        tied = workbook.add_format({"bg_color": "yellow"})
        # ore wa kage
        againstSelf = workbook.add_format({"bg_color": "gray"})
        # Write to the spreadsheet
        for row in range(1, numplayers + 1):
            player_name = sortedPlayers[row - 1].name
            worksheet.write(row, 0, player_name)
            worksheet.write(0, row, player_name)
            for col in range(1, numplayers + 1):
                opponent_name = sortedPlayers[col - 1].name
                ratio = h2h[player_name][opponent_name]
                stringratio = str(ratio[0]) + "-" + str(ratio[1])
                if row == col:
                    worksheet.write(row, col, "", againstSelf)
                elif ratio[0] > ratio[1]:
                    worksheet.write(row, col, str(stringratio), winning)
                elif ratio[1] > ratio[0]:
                    worksheet.write(row, col, str(stringratio), losing)
                elif ratio[0] == 0 and ratio[1] == 0:
                    pass
                else:
                    worksheet.write(row, col, str(stringratio), tied)
        workbook.close()

    def filter_by_games(self, minimum):
        """
        Remove players with below a certain number of games.

        Args:
            eloslist (list of Players): List to be filtered
            minimum (int): Minimum number of games players should have played
                           Anybody with fewer games is removed from the list
        """
        toremove = []
        for player in self.elolist:
            if player.played < minimum:
                toremove.append(player)
        for player in toremove:
            self.elolist.remove(player)

    def filter_by_wins(self, wins):
        """
        Remove entries with less than a certain amount of wins.

        Args:
            eloslist (list of Players): List to be filtered
            wins (int): Minimum number of wins to be left in the list
        """
        toremove = []
        for player in self.elolist:
            if player.won < wins:
                toremove.append(player)
        for player in toremove:
            self.elolist.remove(player)

    def filter_by_rank(self, cutoff):
        """
        Remove entries beyond a certain rank.

        Args:
            eloslist (list of Players): List to be filtered
            cutoff (int): Last rank to keep (e.g. 10 if you want to top 10)
        """
        i = 0
        for player in sorted(self.elolist, key=lambda x: x.elo, reverse=True):
            if i >= cutoff:
                self.elolist.remove(player)
            i += 1

    def filter_by_elo(self, elo):
        """
        Remove entries below a certain elo.

        Args:
            eloslist (list of Players): List to be filtered
            elo (int): Minimum elo to be left in the list
        """
        toremove = []
        for player in self.elolist:
            if player.elo < elo:
                toremove.append(player)
        for player in toremove:
            self.elolist.remove(player)

    def filter_by_tournaments(self, minimum):
        """
        Remove entries who have below a certain number of tournament entries.

        Args:
            eloslist (list of Players): List to be filtered
            minimum (int): Minimum number of tournaments required to remain
        """
        toremove = []
        for player in self.elolist:
            if len(player.placings) < minimum:
                toremove.append(player)
        for player in toremove:
            self.elolist.remove(player)

    def filter_manually(self):
        """
        Open a text editor for the user to manually filter entries.

        If $EDITOR is set, that will be used.
        Otherwise, defers to the system default.
        """
        tempfilename = os.path.join("obj", ".elolisttempfile.txt")
        # Write names to a temp file
        with openFile(tempfilename, "w") as tempfile:
            for player in sorted(self.elolist,
                                 key=lambda x: x.elo, reverse=True):
                tempfile.write(player.name + "\n")
        # Edit the file
        editor = os.environ.get("EDITOR")
        if editor is not None:
            subprocess.call([editor, tempfilename])
        else:
            return
        # Read the remaining names from the file then delete it
        remaining = []
        with openFile(tempfilename, "r") as tempfile:
            for line in tempfile:
                remaining.append(line.strip())
        os.remove(tempfilename)
        # Filter the list
        self.elolist = [p for p in self.elolist if p.name in remaining]

    def write_elos(self, outputfile=os.path.join("output", "elos.txt")):
        """
        Write the elos to a file in a human-readable format.

        By default, this is saved to output/elos.txt.
        """
        outputfilepath = os.path.join(SCRIPTDIR, outputfile)
        with openFile(outputfilepath, "w") as f:
            f.write(str(self))

    def save(self, playersfile=os.path.join("output", "players.pkl")):
        """
        Save the elos (Player data) to a pickle encoded file.

        This can be loaded in for future invocations (e.g. filtering).
        """
        # Pickle file
        playersfilepath = os.path.join(SCRIPTDIR, playersfile)
        with openFile(playersfilepath, "wb") as f:
            pickle.dump(self.elolist,
                        f, pickle.HIGHEST_PROTOCOL)

    def load(self, playersfile=os.path.join("output", "players.pkl")):
        """
        Read player data from a file.

        This should be the file that was saved by elo_list.save().
        """
        players_list = []
        playersfilepath = os.path.join(SCRIPTDIR, playersfile)
        with openFile(playersfilepath, "rb") as f:
            players_list = pickle.load(f)
        self.elolist = players_list

    def summarize(self):
        """
        Print summaries of the players.

        This summary includes information such as rank, elo, and W/L ratio.
        """
        for player in sorted(self.elolist,
                             key=lambda x: x.elo, reverse=True):
            print(player.summary())

    def save_summaries(self, filepath=os.path.join("output", "summaries.txt")):
        """
        Save summaries of the players.

        This summary includes information such as rank, elo, and W/L ratio.
        """
        with openFile(filepath, "w") as f:
            for player in sorted(self.elolist,
                                 key=lambda x: x.elo, reverse=True):
                f.write(player.summary() + "\n")

    def __str__(self):
        """
        Return a nicely formatted representation of this list.

        Information listed is according to str(Player).
        """
        this = "    NAME                  ELO    W    G     W/G     AVG\n"
        rank = 1
        for player in sorted(self.elolist,
                             key=lambda x: x.elo, reverse=True):
            this += "{:>3d}".format(rank) + " " + str(player) + "\n"
            rank += 1
        return this


def openFile(filepath, mode):
    dirpath = pathlib.Path(os.path.dirname(filepath))
    dirpath.mkdir(parents=True, exist_ok=True)
    # DOS-style line endings for non-binary files
    if 'b' not in mode:
        return open(filepath, mode, newline='\r\n')
    return open(filepath, mode)

