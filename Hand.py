HAND_LIMIT = 5

class Hand(object):
    """Hand of cards."""
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """A 'card' is either a Spell, Weapon, or Character."""
        if len(self.cards) >= HAND_LIMIT:
            raise Exception("Too many Cards.")
        self.cards.append(card)

    def __str__(self):
        if not len(self.cards):
            return "Empty"
        out = ""
        for card in self.cards:
            out += "[%d  %s]     " % (card.manaCost, card.name)
	return out
