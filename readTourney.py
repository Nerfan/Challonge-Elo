"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""
import operator

import challonge

# I hope the name is descriptive enough; spaces are optional
# The id is the part of the URL that comes after http://challonge.com/
TOURNAMENT_IDS_SEPARATED_BY_COMMAS\
        = "SmashFrankys3, SFRankysFinals, sf4s, sf4finals1"

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
    
    participants = challonge.participants.index(tournament["id"])
    playersById = {}
    for participant in participants:
        name = participant["display-name"].upper()
        playersById[participant["id"]] = name
        if not name in elos:
            elos[name] = 1200
    
    matches = challonge.matches.index(tournament["id"])
    for match in matches:
        if (match["winner-id"] == match["player1-id"]):
            loserId = match["player2-id"]
        else:
            loserId = match["player1-id"]
        winner = playersById[match["winner-id"]]
        loser = playersById[loserId]
        newElos = calculateWin(elos[winner], elos[loser] )
        elos[winner] = newElos[0]
        elos[loser] = newElos[1]

tourneys = TOURNAMENT_IDS_SEPARATED_BY_COMMAS.replace(" ", "").split(",")
for tourney in tourneys:
    parseTourney(tourney)
printSortedElos()
