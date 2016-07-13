"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""
import operator

import challonge
from player import Player

# I hope the name is descriptive enough; spaces are optional
# The id is the part of the URL that comes after http://challonge.com/
TOURNAMENT_IDS_SEPARATED_BY_COMMAS\
        = "wfw6r2aw, lvrpool1, lvrpool2, lvrpool3, lvrpool4, lvrfinals, r1itlqi3, 833sm0zv, dlt4adcdfsdf, qg42dx64, dlt5jqfjksd, zhywqork, dlt6top5, 3v6ht1tz, dlt7, SmashFrankys3, SFRankysFinals, sf4s, sf4finals1"
DEFAULT_ELO = 1200 # Starting elo for players
import setCredentials # This is a file I made with two lines:
# import challonge
# challonge.set_credentials("USERNAME", "API_KEY")
# USERNAME and API_KEY were replaced with my info, quotes included
# The only reason I made the file is so that I don't accidentally upload my
# challonge API key

# Alternatively, uncomment the folliwing line and add your information:
# challonge.set_credentials("USERNAME", "API_KEY")

aliases = {}
from aliases import aliases # Another file I made with a dictionary
# of replacements for names
# For example, one of the entries is "JEREMY LEFURGE" : "NERFAN"

# Global dictionary to contain elos
# Keys are playernames in all caps, values are elos
playersByName = {}
# Allows players to be accessed by ID
namesById = {}

def parseMatch(match):
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
        winner = playersByName[namesById[match["winner-id"]]]
        loser = playersByName[namesById[match["loser-id"]]]
        winner.calculateWin(loser, score)
        loser.calculateLoss(winner, score)

def printSortedElos():
    """
    Print a sorted list of players in order from highest to lowest elo.
    """
    print("Elos of all players in descending order:")
    print("NAME                  ELO    W    G")
    for player in sorted(list(playersByName.values()),\
            key=lambda x: x.elo, reverse=True):
        print(player.toString())

def parseTourney(tourneyId):
    """
    Calculate elo changes from a tournament.

    Tell the user that a tournament is being parsed.
    Then go through the participants and add them to the record.
    Afterwards, go through each match and find the winner.
    Then calculate elo changes and apply them.

    Args:
        tourneyId (str): The id used in the URL of the tournament
                         i.e. that part after http://challonge.com/
    """
    tournament = challonge.tournaments.show(tourneyId)
    print("Retreiving data from " + tournament["name"] + "...")
    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(tournament["id"])
    
    # Go through participants
    for participant in participants:
        name = participant["display-name"].upper()
        if name in aliases:
            name = aliases[name]
        namesById[participant["id"]] = name
        if not name in playersByName:
            # Adds players to the elo records
            playersByName[name] = Player(name, DEFAULT_ELO, 0, 0)
    
    # Go through matches
    for match in matches:
        parseMatch(match)

def saveElos():
    """
    Save the elos to a file

    Each line of the file is in the form:
    NAME                ELO
    For example:
    JOHN DOE            1200
    """
    file = open("elos.txt", "w")
    file.truncate()
    for player in sorted(list(playersByName.values()),\
            key=lambda x: x.elo, reverse=True):
        file.write(player.toString() + "\n")
    file.close()

def readElos(filename):
    """
    Read pre-existing elos from a file and put them into the elo dictionary

    Assumes that the file is in the format used by saveElos()
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
            playersByName[name] = Player(name, \
                    float(temp[-3]), \
                    int(temp[-2]), \
                    int(temp[-1]))
    file.close()

if __name__ == "__main__":
    filename = input("File to read pre-existing elos from? Blank if none. ")
    if (filename.strip() != ""):
        readElos(filename)
    tourneys = TOURNAMENT_IDS_SEPARATED_BY_COMMAS.replace(" ", "").split(",")
    for tourney in tourneys:
        parseTourney(tourney)
    printSortedElos()
    saveElos()
    if input("Display scores on a graph? (y/n) ") == "y":
        import histogram
        lst = []
        for player in playersByName.values():
            lst.append(player.elo)
        histogram.histogram(lst)
