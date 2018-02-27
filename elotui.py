"""
Provide terminal tools for the elo program.

The name of "User Interface" is a little misleading,
the user doesn't actually interact with this class directly.
They pass arguments to calculate_elos.py
and that script will call the appropriate methods here.
"""

import os
from elo_list import EloList


class EloTUI:
    """
    This class is very simple. It provides a repl to interact with an elo list.

    Store information about the list of elos, nothing else.
    """

    def calculate(self):
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
        elos.export_spreadsheet()
        elos.save()
        elos.write_elos()
        elos.save_summaries()
        print("Elos have been saved to \"output/elos.txt\".")
        print("A MU chart of the top 15 players has been saved to"
              + " \"output/MU Chart.xlsx\".")
        print("Top 15 summaries have been saved to \"output/summaries.txt\".")

    # TODO repl for filtering, summarizing, etc.
    def repl(self):
        return

