#!/usr/bin/python3
"""
Takes data from Challonge to calculate elos of players.

Uses the Challonge public API and pychallonge to parse data.
pychallonge can be found here: https://github.com/russ-/pychallonge
"""

if __name__ == "__main__":
    import elotui
    el = elotui.EloTUI()
    el.main()
