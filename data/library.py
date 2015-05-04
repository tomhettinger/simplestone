"""Library of all possible cards.
"""
from copy import deepcopy

from gameboard.Character import Hero, Minion
from gameboard.Weapon import Weapon
from gameboard.Spell import Spell
from gameboard.Card import Card

heroes = {}
minions = {}
weapons = {}
spells = {}

# Heroes
heroes['rexar'] = Hero("Rexar", 0, 30)
heroes['anduin'] = Hero("Anduin", 0, 30)


# Neutral Minions
#minions[''] = Minion("", )
minions['wisp'] = Minion("Wisp", 1, 1, 0)

minions['boar'] = Minion("Boar", 1, 1, 1, 'charge')
minions['gsFootman'] = Minion("Footman", 1, 2, 1, 'taunt')
minions['shieldbearer'] = Minion("Shldbearer", 0, 4, 1, 'taunt')
minions['yDragonhawk'] = Minion("Y.Drgnhawk", 1, 1, 1, 'windfury')
minions['Argent Squire'] = Minion("ArgentSqre", 1, 1, 1, 'divine')

minions['raptor'] = Minion("Raptor", 3, 2, 2)
minions['bluegill'] = Minion("Bluegill", 2, 1, 2, 'charge')
minions['frostwolf'] = Minion("Frostwolf", 2, 2, 2, 'taunt')
minions['annoyotron'] = Minion("Annoy-o-Tron", 1, 2, 2, ['taunt', 'divine'])

minions['rager'] = Minion("Rager", 5, 1, 3)
minions['wolfrider'] = Minion("Wolfrider", 3, 1, 3, 'charge')
minions['ironfur'] = Minion("Ironfur", 3, 3, 3, 'taunt')
minions['silverback'] = Minion("Silverback", 1, 4, 3, 'taunt')
minions['thrallmar'] = Minion("Thrallmar", 2, 3, 3, 'windfury')
minions['flyingMachine'] = Minion("FlyMachine", 1, 4, 3, 'windfury')
minions['scarletCrusader'] = Minion("ScarletCrus", 3, 1, 3, 'divine')
minions['gnomeregan'] = Minion("Gnomeregan", 1, 4, 3, ['charge', 'taunt'])

minions['yeti'] = Minion("Yeti", 4, 5, 4)
minions['tallstrider'] = Minion("Tallstrider", 5, 4, 4)
minions['stormwindKnight'] = Minion("Knight", 2, 5, 4, 'charge')
minions['mogushan'] = Minion("Mogu'shan", 1, 7, 4, 'taunt')
minions['senjin'] = Minion("Sen'jin", 3, 5, 4, 'taunt')
minions['silvermoonGuardian'] = Minion("SilverMoon", 3, 3, 4, 'divine')

minions['bootyBay'] = Minion("BootyBay", 5, 4, 5, 'taunt')
minions['fenCreeper'] = Minion("FenCreeper", 3, 6, 5, 'taunt')

minions['ogre'] = Minion("Ogre", 6, 7, 6)
minions['rocketeer'] = Minion("Rocketeer", 5, 2, 6, 'charge')
minions['lordOfArena'] = Minion("ArenaLord", 6, 5, 6, 'taunt')
minions['harpy'] = Minion("Harpy", 4, 5, 6, 'windfury')
minions['argentCom'] = Minion("ArgentCom", 4, 2, 6, ['charge', 'divine'])
minions['sunwalker'] = Minion("Sunwalker", 4, 5, 6, ['taunt', 'divine'])

minions['coreHound'] = Minion("CoreHound", 9, 5, 7)

minions['forceTank'] = Minion("Force-Tank", 7, 7, 8, 'divine')

# Weapons
weapons['axe'] = Weapon("Axe", 4, 1, 3)


# Spells
fireball = Spell("Fireball", 4)
fireball.set_effect(spellType="DealDmg", target="anyEnemeyMinion", value=6)
spells['fireball'] = fireball
spells['theCoin'] = Spell("The Coin", 0)


def create_card(name):
    for dictionary in [heroes, minions, weapons, spells]:
        if name in dictionary:
            card = Card(deepcopy(dictionary[name]))
            return card
    raise Exception('%s not found in the library.' % name)


def create_character(name):
    for dictionary in [heroes, minions]:
        if name in dictionary:
            character = deepcopy(dictionary[name])
            return character
    raise Exception('%s not found in the library.' % name)

