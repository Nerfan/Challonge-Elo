"""
Filters elos rankings to a certain subset of players.

Can filter based on number of games played for now.
TODO: filter based on wins, elo, ranking
"""

from player import Player
elos = [] # pylint: disable=invalid-name

def read_elos(filename):
    """
    Read pre-existing elos from a file and put them into the elo dictionary

    Assumes that the file is in the format used by save_elos()

    Args:
        filename (str): Name/path of file beginning in current directory
    """
    file = open(filename)
    for line in file:
        if line.strip() != "":
            temp = line.split()
            name = ""
            for i in range(len(temp)-3):
                name += temp[i] + " "
            name = name.strip()
            elos.append(Player(name,
                               float(temp[-3]),
                               int(temp[-2]),
                               int(temp[-1]))
                       )
    file.close()

def save_elos(filename="elos.txt"):
    """
    Save the elos to a file

    Each line of the file is in the form:
    NAME                ELO
    For example:
    JOHN DOE            1200
    """
    file = open(filename, "w")
    file.truncate()
    for player in sorted(list(elos),
                         key=lambda x: x.elo, reverse=True):
        file.write(str(player) + "\n")
    file.close()

def filter_by_games(minimum):
    """
    Remove entries from the list of elos with below a certain number of games

    Args:
        minimum (int): Minimum number of games players should have played
                       Anybody with fewer games is removed from the elos list
    """
    for player in elos:
        if player.played < minimum:
            elos.remove(player)


read_elos("elos.txt")
filter_by_games(10)
save_elos()
