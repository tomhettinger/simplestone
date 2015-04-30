from random import shuffle as shuf

class Deck(object):
    def __init__(self, side=None):
        self.side = side
        self.cards = []
        self.size = len(self.cards)

    def add_card(self, card):
        self.cards.append(card)
        self.size += 1


    def draw_card(self):
        if self.size <= 0:
            return None
        else:
            self.size -= 1
            return self.cards.pop()


    def shuffle(self):
        shuf(self.cards)
