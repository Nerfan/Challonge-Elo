#!/usr/bin/python3
"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""

import sys
import os
import getopt
from elo_list import EloList

USAGE = "calculate_elos.py [-h] [-t | -g | -w | -r | -e <value>] [-f]\n"\
      + "\t-h\tDisplay this help\n"\
      + "\t-t\tRequire a minimum amount of tournaments\n"\
      + "\t-g\tRequire a minimum amount of games\n"\
      + "\t-w\tRequire a minimum amount of wins\n"\
      + "\t-r\tRequire a minimum rank\n"\
      + "\t-e\tRequire a minimum elo\n"\
      + "\t-f\tManually filter players"

# Maybe list out the args as tuples then statically load them into these
SHORTARGS = "hHt:g:w:r:e:f"
LONGARGS = ["help", "tournaments=", "games=", "wins=", "rank=", "elo=", "filter"]

if __name__ == "__main__":
    minTournament = 0
    minGames = 0
    minWins = 0
    minRank = 0
    minElo = 0
    manualFilter = False

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, SHORTARGS, LONGARGS)
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '-H', '--help'):
            print(USAGE)
            sys.exit(0)
        if opt in ('-t', '--tournaments'):
            minTournament = int(arg)
        if opt in ('-g', '--games'):
            minGames = int(arg)
        if opt in ('-w', '--wins'):
            minWins = int(arg)
        if opt in ('-r', '--rank'):
            minRank = int(arg)
        if opt in ('-e', '--elo'):
            minRank = int(arg)
        if opt in ('-f', '--filter'):
            manualFilter = True

    # Make sure the files to read from actually exist
    if not (os.path.isdir("obj") and os.path.exists("obj/matches.pkl")
            and os.path.exists("obj/participants.pkl")):
        if not os.path.isdir("obj"):
            os.mkdir("obj")
        import save_tourneys
        save_tourneys.main()
    # Create a new EloList object and have that do the work
    elos = EloList()
    elos.calculate_elos()
    if minTournament > 0:
        elos.filter_by_tournaments(minTournament)
    if minGames > 0:
        elos.filter_by_games(minGames)
    if minWins > 0:
        elos.filter_by_wins(minWins)
    if minRank > 0:
        elos.filter_by_rank(minRank)
    if minElo > 0:
        elos.filter_by_elo(minElo)
    if manualFilter:
        elos.filter_manually()
    elos.export_spreadsheet()
    elos.save()
    elos.write_elos()
    elos.save_summaries()
    print("Elos have been saved to \"output/elos.txt\".")
    print("A MU chart of the top 15 players has been saved to"
          + " \"output/MU Chart.xlsx\".")
    print("Top 15 summaries have been saved to \"output/summaries.txt\".")

