"""
In the space, create a strategy for the AI.  The AI looks ahead and evaluates all possible paths
for the next n actions (typically 4).  It then compares the end result of each path and evaluates
which path was the best option, using some function.  The function to evalute the game state 
is one chosen from this module.  You can define whatever startegy you want here.  The input 
parameter is a copy of the game state, along with all contents of the game.  The return value
should be a float, where a larger value is a better path of action than a smaller value.
"""
from random import random


def random_play(boardState):
    """Assign a random value for winStrength. Longer paths will be chosen preferentially,
    since the larger number of nodes means a greater chance of finding a path with a bigger
    random value."""
    winStrength = random()
    return winStrength


def attack_face(boardState):
    """The less health the opponent has, the better.  Still try to add minions to the board,
    when possible though."""
    heroHealth = boardState.get_hero().currentHealth
    enemyHealth = boardState.get_hero(side='enemy').currentHealth
    numberOfMyMinions = len(boardState.get_minions(valid=True))
    # Don't use this path if I'm dead.
    if heroHealth <= 0:
        return -1e6
    # Definitely use this path if opponent is dead.
    elif enemyHealth <= 0:
        return 9000
    # Prioritize health over everything else.
    else:
        return 100.0*(-1.0*enemyHealth) + 1.0*(numberOfMyMinions)


def minion_control(boardState):
    """Remove minions at all cost.  Add 100 points for every minion removed, 10 points for every
    friendly minion added, and 1 point for enemy health removed.  Ignore my own health."""
    heroHealth = boardState.get_hero().currentHealth
    enemyHealth = boardState.get_hero(side='enemy').currentHealth
    minionCount = len(boardState.get_minions(valid=True))
    enemyMinionCount = len(boardState.get_enemy_minions(valid=True))

    if heroHealth <= 0:
        return -1e6
    elif enemyHealth <= 0:
        return 1e6
    else:
        return 100*(-1.0*enemyMinionCount) + 10.0*(minionCount) + 1.0*(-1.0*enemyHealth)
