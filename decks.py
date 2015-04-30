"""Define custom made decks here.
"""
from Deck import Deck
import library

deckContents = {}
deckContents['basic'] = ['boar', 'boar', 'coreHound', 'coreHound', 'raptor', 'raptor', 'axe', 'axe', 'fireball', 'fireball']
deckContents['allBoars'] = ['boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar']


def create_deck(name='basic'):
    thisDeck = Deck()
    for selection in deckContents[name]:
        thisDeck.add_card(library.create_card(selection))
    return thisDeck
