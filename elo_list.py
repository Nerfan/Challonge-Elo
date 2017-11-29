#!/usr/bin/python3
"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""

import os
import os.path
import pickle
from player import Player
from spreadsheet_maker import exportSpreadsheet

from aliases import aliases  # Another file I made with a dictionary
# of replacements for names
# For example, one of the entries is "JEREMY LEFURGE" : "NERFAN"


class EloList:
    """
    Store a list of elos based on input tournaments, then export the info.
    """

    DEFAULT_ELO = 1200 # Starting elo for players

    # Global dictionary to contain elos
    # Keys are playernames in all caps, values are Player objects
    # players_by_name = {}

    # Allows players to be accessed by ID
    # names_by_id = {}

    def __init__(self):
        """
        Constructor method

        Takes no arguments, returns a new EloList object with empty everything.
        """
        self.players_by_name = {}
        self.names_by_id = {}
        self.tournaments = {}

    def read_tournaments_file(self):
        """
        Read obj/tournaments.pkl and create the tournament dictionary.
        """
        with open("obj/tournaments.pkl", "rb") as f:
            tournaments = pickle.load(f)
        for tournament in tournaments:
            self.tournaments[tournament["id"]] = tournament

    def read_players_file(self):
        """
        Read obj/players.pkl and create player dictionaries.

        Assumes that the files exist as created by save_tournaments.py.
        Initializes players_by_name and names_by_id.
        """
        with open("obj/participants.pkl", "rb") as f:
            participants = pickle.load(f)
        # Go through participants
        for participantlist in participants:
            players = 0
            # Check how many players are in the tournament being parsed
            for participant in participantlist:
                players += 1
            for participant in participantlist:
                # Normalize all names
                name = participant["display-name"].upper()
                # Check for known aliases
                if name in aliases:
                    name = aliases[name]
                # Add to a dictionary; key is id; value is name (string, all caps)
                self.names_by_id[participant["id"]] = name
                # If this is a new player, create a new Player object
                if name not in self.players_by_name:
                    self.players_by_name[name] = Player(
                        name, EloList.DEFAULT_ELO, 0, 0, 0
                    )
                # Record the player's performance at the tournament
                # represented by this participant json object.
                self.players_by_name[name].record_tourney(
                    self.tournaments[participant["tournament-id"]],
                    participant
                )

    def read_matches_file(self):
        """
        Read obj/matches.pkl and parse all matches.
        """
        with open("obj/matches.pkl", "rb") as f:
            all_matches = pickle.load(f)
        for tournament in all_matches:
            for match in tournament:
                self.parse_match(match)

    def parse_match(self, match):
        """
        Calculate changes to players from a single match.

        Calculate elo changes and record the match to the Player object
        for head-to-head purposes.

        Args:
            match (json object): Match to take into account to change elos
        """
        if match["winner-id"] != None:
            winner = self.players_by_name[self.names_by_id[match["winner-id"]]]
            loser = self.players_by_name[self.names_by_id[match["loser-id"]]]
            # Calculate elo changes
            # Also record match for head-to-head
            winner.calculateWin(loser, match)
            loser.calculateLoss(winner, match)

    def print_elos(self):
        """
        Print a sorted list of players in order from highest to lowest elo.
        """
        print("Elos of all players in descending order:")
        print("NAME                  ELO    W    G    W/L      AVG")
        for player in sorted(list(self.players_by_name.values()),
                             key=lambda x: x.elo, reverse=True):
            print(player)

    def write_elos(self):
        """
        Save the elos to a file.

        Each line of the file is in the form:
        NAME                ELO
        For example:
        JOHN DOE            1200
        """
        # Pickle file
        with open("obj/players.pkl", "wb") as f:
            pickle.dump(list(self.players_by_name.values()),
                        f, pickle.HIGHEST_PROTOCOL)
        # Human-readable formatted
        file = open("output/elos.txt", "w")
        file.truncate()
        for player in sorted(list(self.players_by_name.values()),
                             key=lambda x: x.elo, reverse=True):
            file.write(str(player) + "\n")
        file.close()

    def read_players(self):
        """
        Read player data from a file.
        """
        players_list = []
        with open("obj/players.pkl", "rb") as f:
            players_list = pickle.load(f)
        for player in players_list:
            name = player.name.upper()
            self.players_by_name[name] = player

    def summarize(self):
        """
        Print summaries of the top 15 players.
        """
        i = 0
        for player in sorted(list(self.players_by_name.values()),
                             key=lambda x: x.elo, reverse=True):
            print(player.summary())
            i += 1
            if i >= 15:
                break

    def main(self):
        # Make sure the files to read from actually exist
        if not (os.path.isdir("obj") and os.path.exists("obj/matches.pkl")
                and os.path.exists("obj/participants.pkl")):
            if not os.path.isdir("obj"):
                os.mkdir("obj")
            import save_tourneys
            save_tourneys.main()
        # Read the files and make the appropriate changes
        self.read_tournaments_file()
        self.read_players_file()
        self.read_matches_file()
        self.write_elos()
        exportSpreadsheet(self.players_by_name.values())
        print("Elos have been saved to \"output/elos.txt\".")
        print("A MU chart of the top 15 players has been saved to \"output/MU Chart.xlsx\".")
        self.summarize()


if __name__ == "__main__":
    calculator = EloList()
    calculator.main()
