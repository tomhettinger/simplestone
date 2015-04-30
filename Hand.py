HAND_LIMIT = 5

class Hand(object):
    """Hand of cards."""
    def __init__(self):
        self.side = None
        self.cards = []
        self.size = 0
        self.board = None


    def add_card(self, card):
        """A 'card' is either a Spell, Weapon, or Character."""
        if len(self.cards) >= HAND_LIMIT:
            raise Exception("Too many Cards.")
        self.cards.append(card)
        self.size += 1


    def remove_card(self, card):
        self.cards.remove(card)


    def __str__(self):
        if not len(self.cards):
            return "Empty"
        out = ""
        for card in self.cards:
            if card.can_play():
                out += "*"
            out += "[%d  %s]     " % (card.contents.manaCost, card.contents.name)
	return out
