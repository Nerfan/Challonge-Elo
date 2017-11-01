#!/usr/bin/python3
"""
Make a matchup spreadsheet of players.

Export in an Excel spreadsheet including colors based on ratio.
HEAVY work in progress
"""

import xlsxwriter


def exportSpreadsheet(players, cutoff=15):
    """
    Export a matchup chart of the top players.

    Write directly to a file named "MU Chart.xlsx."

    Args:
        players:    list of Player objects
        cutoff:     int, number of players to include
    """
    workbook = xlsxwriter.Workbook("output/MU Chart.xlsx")
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
        if i >= cutoff:
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
    # Create color formats for the cells
    # TODO better gradients
    winning = workbook.add_format({"bg_color" : "green"})
    losing = workbook.add_format({"bg_color" : "red"})
    tied = workbook.add_format({"bg_color" : "yellow"})
    # ore wa kage
    againstSelf = workbook.add_format({"bg_color" : "gray"})
    # Write to the spreadsheet
    for row in range(1, cutoff+1):
        player_name = sortedPlayers[row-1].name
        worksheet.write(row, 0, player_name)
        worksheet.write(0, row, player_name)
        for col in range(1, cutoff+1):
            opponent_name = sortedPlayers[col-1].name
            ratio = h2h[player_name][opponent_name]
            stringratio = str(ratio[0]) + "-" + str(ratio[1])
            if row == col:
                worksheet.write(row, col, "", againstSelf)
            elif ratio[0] > ratio[1]:
                worksheet.write(row, col, str(stringratio), winning)
            elif ratio[1] > ratio[0]:
                worksheet.write(row, col, str(stringratio), losing)
            elif ratio[0] == 0 and ratio[1] == 0:
                pass
                #worksheet.write(row, col, str(stringratio))
            else:
                worksheet.write(row, col, str(stringratio), tied)
    workbook.close()
