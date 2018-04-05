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

USAGE = "calculate_elos.py [-h | -i | -s]\n"\
      + "\t-h\tDisplay this help\n"\
      + "\t-i\tRun interactively"

if __name__ == "__main__":
    minTournament = 0


    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hHt:", ["help", "tournaments="])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-h', '-H', '--help']:
            print(USAGE)
            sys.exit(0)
        if opt == '-t':
            minTournament = int(arg)

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
    elos.export_spreadsheet()
    elos.save()
    elos.write_elos()
    elos.save_summaries()
    print("Elos have been saved to \"output/elos.txt\".")
    print("A MU chart of the top 15 players has been saved to"
          + " \"output/MU Chart.xlsx\".")
    print("Top 15 summaries have been saved to \"output/summaries.txt\".")
