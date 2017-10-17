"""
Make a matchup spreadsheet of players.

Export in an Excel spreadsheet including colors based on ratio.
HEAVY work in progress
"""

import xlsxwriter

def exportSpreadsheet(players):
    """
    Export a matchup chart of the top 15 players.

    Args:
        players:    list of Player objects
    Returns:
        a file object, the exported spreadsheet
    """
    NUMPLAYERS = 15
    workbook = xlsxwriter.Workbook("MU Chart.xlsx")
    worksheet = workbook.add_worksheet()
    # Create an array for easy access to ratios, this will be changed later
    # to be in-line
    sortedPlayers = sorted(list(players), key=lambda x: x.elo, reverse=True)
    # Dictionary, keys are names
    #   Values are dictionaries, in which keys are opponent names
    #       Values are tuples of (win, loss)
    # i.e. h2h[player_name][opponent_name] = (wins, losses)
    h2h = {}
    # Loop through all players
    i = 0
    for player in sortedPlayers:
        if i >= NUMPLAYERS:
            break
        ratios = {}
        # Loop through each individual player's head-to-head records
        for opponent in sortedPlayers:
            if opponent in player.h2hwins:
                wins = len(player.h2hwins[opponent])
            else:
                wins = 0
            if opponent in player.h2hlosses:
                losses = len(player.h2hlosses[opponent])
            else:
                losses = 0
            ratios[opponent.name] = (wins, losses)
        i += 1
        h2h[player.name] = ratios
    row = 0
    col = 0
    for row in range(0, NUMPLAYERS):
        for col in range(0, NUMPLAYERS):
            player_name = sortedPlayers[row].name
            opponent_name = sortedPlayers[col].name
            worksheet.write(row, col, str(h2h[player_name][opponent_name]))
    workbook.close()


"""
for each player:
    get matchups for that player, save to a list of dictionaries where the value is a tuple of (win, loss)

structure:
    {name : [{opponent_name : (wins, losses)}]}
For each player in top 15:
    use other top 15 
"""
