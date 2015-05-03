from gameboard import actions


class Action(object):
    """An action consists of a single move."""
    def __init__(self):
        pass


    def perform(self, board):
        """Execute the action on the board."""
        pass



class AttackAction(Action):
    """Attack with a character."""
    def __init__(self, attacker=None, target=None):
        self.attacker = attacker
        self.target = target

    def perform(self, board):
        actions.minion_attack(board, self.attacker, self.target)




class PlayCardAction(Action):
    """Play a card."""



class DoNothingAction(Action):
    """Don't do anything this action."""
    def perform(self, board):
        board.set_text("AI does nothing.")
        pass