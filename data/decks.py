"""Define custom made decks here.
"""
from board.Deck import Deck
import library

deckContents = {}
deckContents['tiny'] = ['boar', 'boar', 'coreHound', 'coreHound', 'raptor', 'raptor', 'axe', 'fireball', ]
deckContents['allBoars'] = ['boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar', 'boar']
deckContents['basic'] = ['wisp', 'wisp', 'boar', 'boar', 'gsFootman', 'gsFootman', 'yDragonhawk', 'yDragonhawk', 'bluegill', 'bluegill', 'raptor', 'raptor', 'flyingMachine', 'flyingMachine', 'silverback', 'silverback', 'yeti', 'yeti', 'senjin', 'senjin', 'stormwindKnight', 'stormwindKnight', 'ogre', 'ogre', 'harpy', 'harpy', 'argentCom', 'argentCom', 'forceTank', 'forceTank']

def create_deck(name='basic'):
    thisDeck = Deck()
    for selection in deckContents[name]:
        thisDeck.add_card(library.create_card(selection))
    return thisDeck
