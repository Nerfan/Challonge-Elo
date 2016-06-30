""" Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""
import operator

import challonge

# I hope the name is descriptive enough; spaces are optional
# The id is the part of the URL that comes after http://challonge.com/
TOURNAMENT_IDS_SEPARATED_BY_COMMAS\
        = "SmashFrankys3, SFRankysFinals, sf4s, sf4finals1"
DEFAULT_ELO = 1200 # Starting elo for players
elos = {}
import setCredentials # This is a file I made with two lines:
# import challonge
# challonge.setCredentials("USERNAME", "API_KEY")
# USERNAME and API_KEY were replaced with my info, quotes included
# You could simply put the second line directly in this file.

def calculateWin(initialWinnerElo, initialLoserElo):
    """
    Calculate changed ELOs based on a win.
    """
    k = 32 # The k factor for elo; larger values mean larger fluctuations
    R1 = 10**(initialWinnerElo/400)
    R2 = 10**(initialLoserElo/400)
    E1 = R1/(R1+R2)
    E2 = R2/(R1+R2)
    finalWinnerElo = initialWinnerElo + k*(1-E1)
    finalLoserElo = initialLoserElo + k*(-E2)
    return (finalWinnerElo, finalLoserElo)

def printSortedElos():
    """
    Print a sorted list of players in order from highest to lowest elo.
    """
    print("Elos of all players in descending order:")
    for elo in sorted(elos, key=elos.get, reverse=True):
        print("{:20s}".format(elo) + "{:04.0f}".format(elos[elo]))

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
    print("Parsing data from " + tournament["name"] + "...")
    
    # Go through participants
    participants = challonge.participants.index(tournament["id"])
    playersById = {} # Allows players to be accessed by ID
    for participant in participants:
        name = participant["display-name"].upper()
        playersById[participant["id"]] = name
        if not name in elos:
            # Adds players to the elo records
            elos[name] = DEFAULT_ELO
    
    # Go through matches
    matches = challonge.matches.index(tournament["id"])
    for match in matches:
        # We need to figure out the ID of the losing player
        if (match["winner-id"] == match["player1-id"]):
            loserId = match["player2-id"]
        else:
            loserId = match["player1-id"]
        # Set variables for easier to read code
        winner = playersById[match["winner-id"]]
        loser = playersById[loserId]
        newElos = calculateWin(elos[winner], elos[loser] )
        elos[winner] = newElos[0]
        elos[loser] = newElos[1]

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
    for elo in elos:
        file.write("{:20s}".format(elo) + str(elos[elo]) + "\n")
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
        temp = line.split()
        name = ""
        for i in range(len(temp)-1):
            name += temp[i]
        elos[name] = float(line.split()[-1])
    file.close()

if __name__ == "__main__":
    filename = input("File to read elos from? Blank if none. ")
    if (filename.strip() != ""):
        readElos(filename)
    tourneys = TOURNAMENT_IDS_SEPARATED_BY_COMMAS.replace(" ", "").split(",")
    for tourney in tourneys:
        parseTourney(tourney)
    printSortedElos()
    saveElos()
