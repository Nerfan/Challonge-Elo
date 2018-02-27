#!/usr/bin/python3
"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""

USAGE = "calculate_elos.py [-h | -i | -s]"\
      + "\t-h\tDisplay this help"\
      + "\t-i\tRun interactively"

if __name__ == "__main__":
    import elotui
    import sys
    import getopt
    argv = sys.argv[1:]
    el = elotui.EloTUI()
    el.calculate()
    try:
        opts, args = getopt.getopt(argv, "hrs", ["ifile=","ofile="])
    except getopt.GetoptError:
        print(USAGE)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(USAGE)
