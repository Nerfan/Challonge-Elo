#!/usr/bin/python3
"""
Given a challonge tournament ID, pulls down the list of participants and seeds
according to a saved elo list.

Participants who do not have any elo records will be seeded at the bottom.
"""

from elo_list import EloList
from player import Player
import challonge
import requests
from aliases import aliases

try:
    import set_credentials
    # This is a file I made with two lines:
    # import challonge
    # challonge.set_credentials("USERNAME", "API_KEY")
    # USERNAME and API_KEY were replaced with my info, quotes included
    # The only reason I made the file is so that I don't accidentally upload my
    # challonge API key
    
    # Alternatively, uncomment the folliwing line and add your information:
    # challonge.set_credentials("USERNAME", "API_KEY")
except ImportError:
    print("File set_credentials.py was not found. Prompting for credentials.")
    print("Information provided will be written out to set_credentials.py.")
    username = input("Username: ")
    apikey = input("API Key: ")
    challonge.set_credentials(username, apikey)
    with open("set_credentials.py", "w") as f:
        f.write("import challonge\n")
        f.write("challonge.set_credentials(\"")
        f.write(username)
        f.write("\", \"")
        f.write(apikey)
        f.write("\")")


def seed(tourney_id):
    elolist = EloList()
    elolist.load()
    players_by_name = {player.name: player for player in elolist.elolist}
    name_to_id = {}
    print("Fetching tournament information...")
    tournament = challonge.tournaments.show(tourney_id)
    participants = challonge.participants.index(tournament["id"])
    seeded = []
    for participant in participants:
        name = participant["name"]
        name_to_id[name] = participant["id"]
        if name.upper() in players_by_name.keys():
            player = players_by_name[name.upper()]
            player.name = name
        else:
            player = Player(name)
            player.elo = 1000
        seeded.append(player)
    seeded = sorted(seeded, key=lambda x: x.elo, reverse=True)
    updatetournament(tourney_id, seeded, name_to_id)


def updatetournament(tourney_id, participants, name_to_id):
    """
    Args:
        tourney_id (str): id of the tournament to set participants for
        participants (list of Players): ordered list of participants
    """
    seed = 1
    for player in participants:
        print("Updating %s as seed %d" % (player.name, seed))
        challonge.participants.update(tourney_id, name_to_id[player.name],
                name=player.name, seed=seed)
        seed += 1


if __name__ == "__main__":
    seed("nerfanTest")
