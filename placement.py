class Placement:
    """
    Represent a value object for a single placement for a single player.

    This class holds information about how a player performed
    at a single tournament.

    Fields include:
    playername:     string
    tourney:        tournament json object
    placement:      int
    entrants:       int
    loss1:          Player object
    loss2:          Player object
    """

    def __init__(self, pname, tourney, participant):
        self.playername = pname
        self.tourney = tourney
        self.entrants = tourney["participants-count"]
        self.placement = participant["final-rank"]
        self.loss1 = None
        self.loss2 = None

    def __str__(self):
        string = ""
        string += str(self.placement) + " at '"
        string += self.tourney["name"] + "'"
        if self.loss1 is not None:
            string += " (Lost to " + self.loss1.name
            if self.loss2 is not None:
                string += " and " + self.loss2.name
            string += ")"
        return string
