class Card(object):
    def __init__(self, contents=None):
        self.contents = contents
        self.board = None
        self.side = None

    def can_play(self):
        playerTurn = self.board.playerTurn
        availMana = self.board.manaCurrent[playerTurn]
        cost = self.contents.manaCost
        return (self.side == playerTurn) and (cost <= availMana)

    def set_contents(self, contents):
        """Set the contents of a card (weapon, spell, minion)."""
        self.contents = contents
