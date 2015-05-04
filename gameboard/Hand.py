HAND_LIMIT = 10

class Hand(object):
    """Hand of cards."""
    def __init__(self):
        self.side = None
        self.cards = []
        self.size = 0
        self.board = None
        self.CPU = False


    def get_card(self, pos):
        """Return the card at the pos (idx+1) specified."""
        return self.cards[pos-1]


    def get_playable_cards(self):
        """Return a list of the cards that can be played."""
        playableCards = []
        for card in self.cards:
            if card.can_play():
                 playableCards.append(card)
        return playableCards


    def get_playable_card_positions(self):
        """Return the position (idx+1) of the cards that can be played."""
        playableCardPos = []
        for i, card in enumerate(self.cards):
            if card.can_play():
                 playableCardPos.append(i+1)
        return playableCardPos


    def add_card(self, card):
        """A 'card' is either a Spell, Weapon, or Character."""
        if len(self.cards) >= HAND_LIMIT:
            raise Exception("Too many Cards.")
        self.cards.append(card)
        self.size += 1
        card.hand = self

    def remove_card(self, card):
        self.cards.remove(card)


    def is_full(self):
        return self.size >= HAND_LIMIT


    def __str__(self):
        if not len(self.cards):
            return "Empty"
        out = ""

        if self.CPU:
            for card in self.cards:
                out += "| ??? |"
        else:
            for card in self.cards:
                if card.can_play():
                    out += "*"
                out += "|{%d} %s|  " % (card.contents.manaCost, card.contents.name)

        return out
