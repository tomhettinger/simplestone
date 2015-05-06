import time, random

import gameboard.loop as loop
from gameboard.Character import Character
from gameboard.Spell import Spell
from DecisionTree import DecisionTree as DT
import Action


class AI(object):
    """An artificial intellegince for playing out turns in SimpleStone."""
    def __init__(self, strategy=None, name="Dave"):
        self.strategy = strategy
        self.name = name


    def play_turn(self, board):
        """Execute all of the actions on the board for this turn, then end the turn 
        and give the game back to the human."""
        while True:
            loop.refresh(board)
            time.sleep(0.3)

            # Check if we have lethal.
            #lethalActions = check_for_lethal(board)
            #if lethalActions is not None:
            #    lethalActions[0].perform(board)
            #    continue

            tree = DT(board, strategy=self.strategy)
            bestAction = tree.bestAction
            del tree
            if bestAction is None:  # No more available actions.
                break
            if isinstance(bestAction, Action.DoNothingAction):
                bestAction.perform(board)
                break
            bestAction.perform(board)
        loop.end_turn(board)


    def check_for_lethal(self, board):
        """Naively check if the available attacks on the enemy Hero added up will kill him.  If a possible
        lethal in a couple actions is possible, it will be found be the tree anyway."""
        pass
        # Get available actions
        # Find actions that damage the enemy hero.
        # Compare total damage with health
        # if HeroDies:
        #     return the list of actions.
        # else:
        #     return None