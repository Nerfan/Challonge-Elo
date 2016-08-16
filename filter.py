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

def filter_by_games(eloslist, minimum):
    """
    Remove entries from the list of elos with below a certain number of games

    Args:
        eloslist (list of Players): List to be filtered
        minimum (int): Minimum number of games players should have played
                       Anybody with fewer games is removed from the elos list

    Returns:
        list of Players who have played at least the minumum games
    """
    for player in eloslist:
        if player.played < minimum:
            eloslist.remove(player)
    return eloslist

def filter_by_rank(eloslist, cutoff):
    """
    Remove entries beyond a certain rank

    Args:
        eloslist (list of Players): List to be filtered
        cutoff (int): Last rank to keep (e.g. 10 if you want to top 10)

    Returns:
        list of Players who are ranked at or above the cutoff
    """
    i = 0
    for player in sorted(list(eloslist), key=lambda x: x.elo, reverse=True):
        if i >= cutoff:
            eloslist.remove(player)
        i += 1
    return eloslist

def filter_by_elo(eloslist, elo):
    """
    Remove entries below a certain elo

    Args:
        eloslist (list of PLayers): List to be filtered
        elo (int): Minimum elo to be left in the list

    Returns:
        list of Players who have at least the given elo
    """
    for player in eloslist:
        if player.elo < elo:
            eloslist.remove(player)
    return eloslist


read_elos("elos.txt")
filter_by_games(elos, 10)
save_elos()
