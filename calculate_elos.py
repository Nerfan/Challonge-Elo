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

# Both of these are in the form (option, description)
OPTS = [  # Options that don't require an argument
    ("filter", "Manually filter players"),
]
ARGOPTS = [  # Options that require an argument
    ("tournaments", "Require a minimum amount of tournaments"),
    ("games", "Require a minimum amount of games"),
    ("wins", "Require a minimum amount of wins"),
    ("rank", "Require a minimum rank"),
    ("elo", "Require a minimum elo"),
]

# Programatically create the usage statement and appropriate options
USAGE = "calculate_elos.py [options]\nOptions:"\
        "\n\t-h\tDisplay this help"
SHORTARGS = ""
LONGARGS = []
for opt in OPTS:
    USAGE += "\n\t-" + opt[0][0] + "\t" + opt[1]
    SHORTARGS += opt[0][0]
    LONGARGS.append(opt[0])
for opt in ARGOPTS:
    USAGE += "\n\t-" + opt[0][0] + "\t" + opt[1]
    SHORTARGS += opt[0][0] + ":"
    LONGARGS.append(opt[0] + "=")


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, SHORTARGS, LONGARGS)
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)

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
    for opt, arg in opts:
        if opt.strip('-')[0] == 't':  # Tournaments
            elos.filter_by_tournaments(int(arg))
        if opt.strip('-')[0] == 'g':  # Games
            elos.filter_by_games(int(arg))
        if opt.strip('-')[0] == 'w':  # Wins
            elos.filter_by_wins(int(arg))
        if opt.strip('-')[0] == 'r':  # Rank
            elos.filter_by_rank(int(arg))
        if opt.strip('-')[0] == 'e':  # Elo
            elos.filter_by_elo(int(arg))
        if opt.strip('-')[0] == 'f':  # Manual filtering
            elos.filter_manually()
    elos.export_spreadsheet()
    elos.save()
    elos.write_elos()
    elos.save_summaries()
    print("Elos have been saved to \"output/elos.txt\".")
    print("A MU chart of all players has been saved to"
          + " \"output/MU Chart.xlsx\".")
    print("Player summaries have been saved to \"output/summaries.txt\".")

