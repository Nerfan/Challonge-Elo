"""
Use data taken from Challonge to calculate elos for players

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""

import pickle
from player import Player

from aliases import aliases  # Another file I made with a dictionary
# of replacements for names
# For example, one of the entries is "JEREMY LEFURGE" : "NERFAN"


class EloCalculator:
    """
    Calculate and store a list of elos based on input tournaments.

    Methods are provided to save and retrive elo data as well.
    """

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

    def read_tournaments_file(self, tournamentfile):
        """
        Read obj/tournaments.pkl and create the tournament dictionary.
        """
        with open(tournamentfile, "rb") as f:
            tournaments = pickle.load(f)
        for tournament in tournaments:
            self.tournaments[tournament["id"]] = tournament

    def read_participants_file(self, participantsfile):
        """
        Read obj/participants.pkl and create player dictionaries.

        Assumes that the files exist as created by save_tournaments.py.
        Initializes players_by_name and names_by_id.
        """
        with open(participantsfile, "rb") as f:
            participants = pickle.load(f)
        # Go through participants
        for participantlist in participants:
            players = 0
            # Check how many players are in the tournament being parsed
            for participant in participantlist:
                players += 1
            # Add the player to the dictionaries
            for participant in participantlist:
                # Normalize all names
                name = participant["display-name"].upper()
                # Check for known aliases; allow transitive property
                while name in aliases:
                    name = aliases[name]
                # Add to reference dictionaries and update data
                self.names_by_id[participant["id"]] = name
                if name not in self.players_by_name:
                    self.players_by_name[name] = Player(name)
                self.players_by_name[name].record_tourney(
                    self.tournaments[participant["tournament-id"]],
                    participant
                )

    def read_matches_file(self, matchesfile):
        """
        Read obj/matches.pkl and parse all matches.
        """
        with open(matchesfile, "rb") as f:
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

    def calculate(self, tournamentfile, participantsfile, matchesfile):
        """
        Run the calculations.
        """
        self.read_tournaments_file(tournamentfile)
        self.read_participants_file(participantsfile)
        self.read_matches_file(matchesfile)

    def set_elo_list(self, elolist):
        """
        Set the values of the dictionary that stores Player objects.

        This effectively "resets" all of the elos to the ones provided.
        Since this resets, it deletes the old data.
        """
        self.players_by_name.clear()
        for player in elolist:
            self.players_by_name[player.name.upper()] = player

    def get_elo_list(self):
        """
        Return the list of all Player objects.
        """
        return list(self.players_by_name.values())
