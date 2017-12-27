"""
Provide a terminal user interface for the elo program.
"""

import os
from elo_list import EloList


class EloTUI:
    """
    This class is very simple. It provides a repl to interact with an elo list.

    Store information about the list of elos, nothing else.
    """

    def main(self, argv=[]):
        """
        Calculate elos and save them to a file.
        """
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
        elos.exportSpreadsheet()
        elos.save()
        elos.write_elos()
        print("Elos have been saved to \"output/elos.txt\".")
        print("A MU chart of the top 15 players has been saved to"
              + " \"output/MU Chart.xlsx\".")
        if len(argv) > 0:
            if argv[0] == "-r":
                self.repl()

    # TODO repl for filtering, summarizing, etc.
    def repl(self):
        return
