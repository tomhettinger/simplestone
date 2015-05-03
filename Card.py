class Card(object):
    def __init__(self, contents=None):
        self.contents = contents
        self.hand = None
        if contents is not None:
            self.name = contents.name


    def can_play(self):
        side = self.hand.board.playerTurn
        availMana = self.hand.board.manaCurrent[side]
        cost = self.contents.manaCost
        return (self.hand.side == self.hand.board.get_side()) and (cost <= availMana)


    def set_contents(self, contents):
        """Set the contents of a card (weapon, spell, minion)."""
        self.contents = contents
        self.name = contents.name
