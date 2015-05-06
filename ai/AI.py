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
            time.sleep(1)
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


    def select_random_action(self, actions):
        """Of the actions, choose one randomly and perform it."""
        return random.choice(actions)
