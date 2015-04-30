MAX_MINIONS = 4

class Board(object):
    """Board class which holds minions on it (4 per side) and Heros."""

    def __init__(self, topHero=None, bottomHero=None):
        self.heroes = {'top':topHero, 'bottom':bottomHero}
        self.decks = {'top':None, 'bottom':None}
        self.hands = {'top':None, 'bottom':None}
        self.manaBase = {'top':1, 'bottom':1}
        self.manaCurrent = {'top':1, 'bottom':1} 
        self.minions = {'top':[None, None, None, None], 'bottom':[None, None, None, None]}
        self.playerTurn = 'bottom'
        self.turnCount = 1
        self.outputText = ""

    def __str__(self):
        out = "\n\n"
        out += "{:^100}".format("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        out += "\n"
        handOut = "Deck: %d   " % self.decks['top'].size
        handOut += str(self.hands['top'])
        manaOut = "Mana: %d/%d" % (self.manaCurrent['top'], self.manaBase['top'])
        out += "{:<85}{:>15}".format(handOut, manaOut)
        out += "\n\n"
        if self.heroes['top'] is None:
            out += "{:^100}".format("None")
        else:
            out += "{:^100}".format(str(self.heroes['top']))
        out += " \n\n\n\n"

        minionOut = []
        for m in self.minions['top']:
            if m is None:
                minionOut.append("____")
            else:
                minionOut.append(str(m))
        out += "{:^25}{:^25}{:^25}{:^25}".format(*minionOut)
        out += "\n\n"
        minionOut = []
        for m in self.minions['bottom']:
            if m is None:
                minionOut.append("____")
            else:
                minionOut.append(str(m))
        out += "{:^25}{:^25}{:^25}{:^25}".format(*minionOut)
        out += "\n\n\n\n"

        if self.heroes['bottom'] is None:
            out += "{:^100}".format("None")
        else:
            out += "{:^100}".format(str(self.heroes['bottom']))
        out += "\n\n"
        handOut = "Deck: %d   " % self.decks['bottom'].size
        handOut += str(self.hands['bottom'])
        manaOut = "Mana: %d/%d" % (self.manaCurrent['bottom'], self.manaBase['bottom'])
        out += "{:<85}{:>15}".format(handOut, manaOut)
        out += "\n"
        out += "{:^100}".format("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        out += "\n"
        out += "{:<100}".format(self.outputText)
        out += "\n"

        return out


    def set_hand(self, hand, side):
        self.hands[side] = hand
        hand.side = side
        hand.board = self


    def set_deck(self, deck, side):
        self.decks[side] = deck
        deck.side = side


    def set_hero(self, character, side):
        """Set a hero with a given character object."""
        if self.heroes[side] is not None:
            raise Exception
        self.heroes[side] = character
        character.side = side
        character.board = self


    def set_minion(self, character, side, pos=None):
        """Place a minion on the board given the side and (optional) position. If position
        is not specified, place the minion in lowest available spot (not implemented yet)."""
        if self.minions[side][pos] is not None:
            raise Exception
        self.minions[side][pos] = character
        character.side = side
        character.board = self


    def destroy_minion(self, character):
        """Destroy the character specified from the field."""
        for i, c in enumerate(self.minions['top']):
            if c is character:
                self.minions['top'][i] = None
                character.deathrattle()
                del character
                break
