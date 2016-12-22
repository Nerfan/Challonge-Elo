#!/usr/bin/python3.5
"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""

import challonge
from player import Player


import setCredentials # This is a file I made with two lines:
# import challonge
# challonge.set_credentials("USERNAME", "API_KEY")
# USERNAME and API_KEY were replaced with my info, quotes included
# The only reason I made the file is so that I don't accidentally upload my
# challonge API key

# Alternatively, uncomment the folliwing line and add your information:
# challonge.set_credentials("USERNAME", "API_KEY")

from aliases import aliases # Another file I made with a dictionary
# of replacements for names
# For example, one of the entries is "JEREMY LEFURGE" : "NERFAN"

from tournamentlist import tourneys # And again, same case as aliases
# Just a list if strings instead of a dictionary.
# The strings represent the tournement.
# For each tournament, the string to enter is the part of the URL after
# http://challonge.com/
# For example, if your URL is http://challonge.com/wfw6r2aw,
# enter wfw6r2aw as a string into the list.

DEFAULT_ELO = 1200 # Starting elo for players

# Global dictionary to contain elos
# Keys are playernames in all caps, values are Player objects
players_by_name = {}
# Allows players to be accessed by ID
names_by_id = {}

def parse_match(match):
    """
    Calculate changes on elo from a single match

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

def parse_tourney(tourney_id):
    """
    Calculate elo changes from a tournament.

    Tell the user that a tournament is being parsed.
    Then go through the participants and add them to the record.
    Afterwards, go through each match and find the winner.
    Then calculate elo changes and apply them.

    Args:
        tourney_id (str): The id used in the URL of the tournament
                         i.e. that part after http://challonge.com/
    """
    tournament = challonge.tournaments.show(tourney_id)
    print("Retreiving data from " + tournament["name"] + "...")
    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(tournament["id"])

    # Go through participants
    for participant in participants:
        name = participant["display-name"].upper()
        if name in aliases:
            name = aliases[name]
        names_by_id[participant["id"]] = name
        if not name in players_by_name:
            # Adds players to the elo records
            players_by_name[name] = Player(name, DEFAULT_ELO, 0, 0)

    # Go through matches
    for match in matches:
        parse_match(match)

def save_elos():
    """
    Save the elos to a file

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

if __name__ == "__main__":
    #filename = input("File to read pre-existing elos from? Blank if none. ")
    filename = ""
    if filename.strip() != "":
        read_elos(filename)
    for tourney in tourneys:
        parse_tourney(tourney)
    while True:
        playername = input("Whose records would you like to see? ")
        playername = playername.upper()
        if playername == "":
            break
        if playername not in players_by_name:
            print("Error: " + playername + " not found.")
        else:
            print(players_by_name[playername].h2h_list())
            while True:
                details = input("Would you like detailed information " \
                                + "about a specific head-to-head? ")
                details = details.upper()
                if details == "":
                    break;
                if details not in players_by_name:
                    print("Error: " + details + " not found.")
                else:
                    other = players_by_name[details]
                    print(players_by_name[playername].h2h_details(other))
#    if input("Display scores on a graph? (y/n) ") == "y":
#        import histogram
#        lst = []
#        for player in players_by_name.values():
#            lst.append(player.elo)
#        histogram.histogram(lst)
