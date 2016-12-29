#!/usr/bin/python3.5
"""
Save the calculated data from a list of tournaments for easy reference.

Collects data on players and matches.
Saves to three separate files.
"""

import pickle
import challonge

import setCredentials # This is a file I made with two lines:
# import challonge
# challonge.set_credentials("USERNAME", "API_KEY")
# USERNAME and API_KEY were replaced with my info, quotes included
# The only reason I made the file is so that I don't accidentally upload my
# challonge API key

# Alternatively, uncomment the folliwing line and add your information:
# challonge.set_credentials("USERNAME", "API_KEY")

from tournamentlist import tourneys # And again, same case as aliases
# Just a list if strings instead of a dictionary.
# The strings represent the tournement.
# For each tournament, the string to enter is the part of the URL after
# http://challonge.com/
# For example, if your URL is http://challonge.com/wfw6r2aw,
# enter wfw6r2aw as a string into the list.

# List of all participants in all tournaments
# This is a list of lists; each list represents a tournament
# and the objects within represent a player.
raw_participants = []
# List of all matches
# This is a list of lists; each list represents a tournament
# and the objects within represent a match.
all_matches = []


def read_tourney(tourney_id):
    """
    Get info about a tournament through the challonge api.

    Saves the participants and matches to be processed later.

    Args:
        tourney_id (str): The id used in the URL of the tournament
                         i.e. that part after http://challonge.com/
    """
    tournament = challonge.tournaments.show(tourney_id)
    print("Retreiving data from " + tournament["name"] + "...")
    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(tournament["id"])

    # Go through participants
    raw_participants.append(participants)

    # Go through matches
    all_matches.append(matches)

def main():
    """
    Read and save data from tourneys defined in tournamentlist.py
    """
    for tourney in tourneys:
        read_tourney(tourney)
    with open("obj/participants.pkl", "wb") as f:
        pickle.dump(raw_participants, f, pickle.HIGHEST_PROTOCOL)
    with open("obj/matches.pkl", "wb") as f:
        pickle.dump(all_matches, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main()
