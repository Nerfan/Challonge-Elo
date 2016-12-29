from calculate_elos import *

def eloTomorrow(winner, loser, set):
    """
    Calculates elo changes if any two players play a set.
    :Player param winner: winner of the hypothetical set
    :Player param loser: loser of the hypothetical set
    :str param set: 3-0, 3-1, 3-2, 2-1, or 2-0, game win count.
    :tuple return: hypothetical updated elo's of (winner, loser). Nothing is saved in the player object.
    """
    p1elo = winner.elo
    p2elo = loser.elo
    k=32
    R1 = 10**(winner.elo/400)
    R2 = 10**(loser.elo/400)
    winE1 = R1/(R1+R2)
    loseE1 = R2/(R1+R2)
    winresult = 1.25
    loseresult = 0
    if set in ["2-0", "3-1"]:
        winresult = 1.25
        loseresult = 0
    elif set in ["2-1", "3-2"]:
        winresult = 1
        loseresult = .33
    elif set in ["3-0"]:
        winresult = 1.5
        loseresult = -.25
    p1elo = p1elo + k*(winresult-winE1)
    p2elo = p2elo + k*(loseresult-loseE1)

    return p1elo, p2elo

if __name__ == "__main__":
    for tourney in tourneys:
        parse_tourney(tourney)
    save_elos()
    while True:
        while True:
            p1 = input("Enter winner: ")
            p1 = p1.upper()
            if p1 not in players_by_name:
                print("Error: " + p1 + " not found.")
                print()
                break
            p2 = input("Enter loser: ")
            p2 = p2.upper()
            if p2 not in players_by_name:
                print("Error: " + p2 + " not found.")
                print()
                break
            set = input("Enter set result: ")
            if set not in ["2-0", "3-1", "2-1", "3-2", "3-0"]:
                print("Error: " + set + " is invalid.")
                print()
                break

            new_elo = eloTomorrow(players_by_name[p1], players_by_name[p2], set)
            print()
            print(p1 + "'s elo was " + "{:0>4.0f}".format(players_by_name[p1].elo) + ", and would be: " + \
                  "{:0>4.0f}".format(new_elo[0]))
            print(p2 + "'s elo was " + "{:0>4.0f}".format(players_by_name[p2].elo) + ", and would be: " + \
                  "{:0>4.0f}".format(new_elo[1]))
            print()

