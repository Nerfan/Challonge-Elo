"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""
import operator

import challonge
import boxAndWhisker

# I hope the name is descriptive enough; spaces are optional
# The id is the part of the URL that comes after http://challonge.com/
TOURNAMENT_IDS_SEPARATED_BY_COMMAS\
        = "wfw6r2aw, lvrpool1, lvrpool2, lvrpool3, lvrpool4, lvrfinals, r1itlqi3, 833sm0zv, dlt4adcdfsdf, qg42dx64, dlt5jqfjksd, zhywqork, dlt6top5, 3v6ht1tz, dlt7, SmashFrankys3, SFRankysFinals, sf4s, sf4finals1"
DEFAULT_ELO = 1200 # Starting elo for players

# Global dictionary to contain elos
# Keys are playernames in all caps, values are elos
elos = {}

import setCredentials # This is a file I made with two lines:
# import challonge
# challonge.set_credentials("USERNAME", "API_KEY")
# USERNAME and API_KEY were replaced with my info, quotes included
# Alternatively, uncomment the folliwing line and add your information:
# challonge.set_credentials("USERNAME", "API_KEY")

aliases = {}
from aliases import aliases # Another file I made with a dictionary
# of replacements for names
# For example, one of the entries is "JEREMY LEFURGE" : "NERFAN"

def drawBoxAndWhisker():
    """
    Plot the elo scores on a box and whisker plot
    """
    scores = list(elos.values())
    scores.sort()
    medianIndex = len(scores)//2
    q1Index = medianIndex//2
    q3Index = medianIndex + q1Index
    boxAndWhisker.boxAndWhisker(
            scores[0],
            scores[q1Index], 
            scores[medianIndex], 
            scores[q3Index], 
            scores[-1])

def calculateWin(initialWinnerElo, initialLoserElo):
    """
    Calculate changed ELOs based on a win.

    Args:
        initialWinnerElo (float): Elo of the winner before this calculation
        initialLoserElo (float): Elo of the loser before this calculation

    Returns:
        Tuple in the form (winnerElo, loserElo)
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
    print("Retreiving data from " + tournament["name"] + "...")
    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(tournament["id"])
    
    # Go through participants
    playersById = {} # Allows players to be accessed by ID
    for participant in participants:
        name = participant["display-name"].upper()
        if name in aliases:
            name = aliases[name]
        playersById[participant["id"]] = name
        if not name in elos:
            # Adds players to the elo records
            elos[name] = DEFAULT_ELO
    
    # Go through matches
    for match in matches:
        if match["winner-id"] != None:
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
    for elo in sorted(elos, key=elos.get, reverse=True):
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
        if line.strip() != "":
            temp = line.split()
            name = ""
            for i in range(len(temp)-1):
                name += temp[i] + " "
            name = name.strip()
            elos[name] = float(line.split()[-1])
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
    drawBoxAndWhisker()
