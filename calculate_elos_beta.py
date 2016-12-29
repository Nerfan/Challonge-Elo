#!/usr/bin/python3.5
"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""

import os
import os.path
import pickle
from player import Player

from aliases import aliases # Another file I made with a dictionary
# of replacements for names
# For example, one of the entries is "JEREMY LEFURGE" : "NERFAN"

DEFAULT_ELO = 1200 # Starting elo for players

# Global dictionary to contain elos
# Keys are playernames in all caps, values are elos
players_by_name = {}
# Allows players to be accessed by ID
names_by_id = {}
# List of all matches
all_matches = []

def read_tournaments():
    """
    Read information from pickle files.

    Assumes that the files exist as created by save_tournaments.py.
    Initializes players_by_name, names_by_id, and all_matches.
    """
    # Tell python that we want to use the global variables
    global players_by_name
    global names_by_id
    global all_matches
    with open("obj/participants.pkl", "rb") as f:
        participants = pickle.load(f)
    with open("obj/matches.pkl", "rb") as f:
        all_matches = pickle.load(f)
    # Go through participants
    for participant in participants:
        # Normalize all names
        name = participant["display-name"].upper()
        # Check for known aliases
        if name in aliases:
            name = aliases[name]
        # Add to a dictionary; key is id; value is name (string, all caps)
        names_by_id[participant["id"]] = name
        # If this is a new player, create a Player object to represent them
        if not name in players_by_name:
            players_by_name[name] = Player(name, DEFAULT_ELO, 0, 0)

def parse_match(match):
    """
    Calculate changes to players from a single match.

    Calculate elo changes and record the match to the Player object
    for head-to-head purposes.

    Args:
        match (json object): Match to take into account to change elos
    """
    if match["winner-id"] != None:
        if match["scores-csv"] != None:
            score = match["scores-csv"]
        else:
            score = "1-0"
        # Make sure score is within a reasonable range to protect against dq's
        if score not in ["1-0", "2-0", "3-0", "2-1", "3-1", "3-2",
                         "0-1", "0-2", "0-3", "1-2", "1-3", "2-3"]:
            return
        winner = players_by_name[names_by_id[match["winner-id"]]]
        loser = players_by_name[names_by_id[match["loser-id"]]]
        # Calculate elo changes
        winner.calculateWin(loser, score)
        loser.calculateLoss(winner, score)
        # Record match for head-to-head
        if loser not in winner.h2hwins:
            winner.h2hwins[loser] = []
        winner.h2hwins[loser].append(match)
        if winner not in loser.h2hlosses:
            loser.h2hlosses[winner] = []
        loser.h2hlosses[winner].append(match)

def print_elos():
    """
    Print a sorted list of players in order from highest to lowest elo.
    """
    print("Elos of all players in descending order:")
    print("NAME                  ELO    W    G")
    for player in sorted(list(players_by_name.values()),
                         key=lambda x: x.elo, reverse=True):
        print(player)

def save_elos():
    """
    Save the elos to a file.

    Each line of the file is in the form:
    NAME                ELO
    For example:
    JOHN DOE            1200
    """
    file = open("elos.txt", "w")
    file.truncate()
    for player in sorted(list(players_by_name.values()),
                         key=lambda x: x.elo, reverse=True):
        file.write(str(player) + "\n")
    file.close()

def read_elos(filename):
    """
    Read pre-existing elos from a file and put them into the elo dictionary

    Assumes that the file is in the format used by save_elos()

    Args:
        filename (str): Name/path of file beginning in current directory
    """
    file = open(filename)
    for line in file:
        if line.strip() != "":
            temp = line.split()
            name = ""
            for i in range(len(temp)-3):
                name += temp[i] + " "
            name = name.strip()
            players_by_name[name] = Player(name,
                                           float(temp[-3]),
                                           int(temp[-2]),
                                           int(temp[-1]))
    file.close()

# "Main" functions

def init():
    """
    Initialize Player data based on tournaments that were read before.

    Assumes obj/ was filled by save_tournaments.py.
    Fills global dictionaries and edits based on matches.

    If Python sees that the directory/files do not exist,
    then the tournament data is read now.
    """
    if not (os.path.isdir("obj") and os.path.exists("obj/matches.pkl")
            and os.path.exists("obj/participants.pkl")):
        if not os.path.isdir("obj"):
            os.mkdir("obj", exist_ok=True)
        import save_tourneys
        save_tourneys.main()
    read_tournaments()
    for match in all_matches:
        parse_match(match)

def elos():
    """
    Print and save elos.
    """
    print_elos()
    save_elos()
    # TODO stuff with filtering

def h2h():
    """
    Ask the user if they would like to see head-to-head statistics.
    """
    while True: # Loop until we break out of it
        playername = input("Whose records would you like to see? ")
        playername = playername.upper()
        if playername == "": # Break on no input
            break
        if playername not in players_by_name: # Need a real player
            print("Error: " + playername + " not found.")
        else:
            print(players_by_name[playername].h2h_list())
            while True: # Ask for details
                details = input("Would you like detailed information " \
                                + "about a specific head-to-head? ")
                details = details.upper()
                if details == "": # Break on no input
                    break
                if details not in players_by_name: # Need a real player
                    print("Error: " + details + " not found.")
                else:
                    other = players_by_name[details]
                    print(players_by_name[playername].h2h_details(other))


if __name__ == "__main__":
    init()
    elos()
    h2h()
