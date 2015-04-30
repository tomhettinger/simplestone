from copy import deepcopy

from Character import Hero, Minion
from Weapon import Weapon
from Spell import Spell
from Card import Card

heroes = {}
minions = {}
weapons = {}
spells = {}

# Heroes
heroes['rexar'] = Hero("Rexar", 0, 30)
heroes['anduin'] = Hero("Anduin", 0, 30)

# Minions
minions['boar'] = Minion("Boar", 1, 1, 1)
minions['raptor'] = Minion("Raptor", 2, 3, 2)
minions['coreHound'] = Minion("Core Hound", 9, 5, 7)

# Weapons
weapons['axe'] = Weapon("Axe", 4, 1, 3)

# Spells
fireball = Spell("Fireball", 4)
fireball.set_effect(spellType="DealDmg", target="anyEnemeyMinion", value=6)
spells['fireball'] = fireball


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

