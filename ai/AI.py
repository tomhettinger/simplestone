import time, random

import gameboard.loop as loop
import Action

class AI(object):
    """An artificial intellegince for playing out turns in SimpleStone."""
    def __init__(self):
        self.name = "Dave"

    def play_turn(self, board):
        """Execute all of the actions on the board for this turn, then end the turn 
        and give the game back to the human."""
        # DUMB AI:
        # Select a random action until there are no more actions to be done.
        availableActions = self.get_available_actions(board)
        randomAction = self.select_random_action(availableActions)
        randomAction.perform(board)
        loop.refresh(board)
        time.sleep(2)
        loop.end_turn(board)


    def get_available_actions(self, board):
        """Find out every possible action for this instant."""
        cardPlayActions = self.get_card_play_actions(board)
        attackActions = self.get_attack_actions(board)
        availableActions = [Action.DoNothingAction()]
        availableActions.extend(cardPlayActions)
        availableActions.extend(attackActions)
        #availableActions.extend(heroAbilityActions)
        return availableActions


    def get_attack_actions(self, board):
        """Find all possible attack combinations and return a list of them."""
        actionList = []
        potentialAttackers = board.get_canAttack_characters()
        if not len(potentialAttackers):
            return []
        for character in potentialAttackers:
            potentialTargets = board.get_targetable_characters(character)
            if not len(potentialTargets):
                continue
            for target in potentialTargets:
                actionList.append(Action.AttackAction(character, target))
        return actionList


    def get_card_play_actions(self, board):
        return [Action.DoNothingAction()]


    def select_random_action(self, actions):
        """Of the actions, choose one randomly and perform it."""
        return random.choice(actions)
