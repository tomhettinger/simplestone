from gameboard import actions


class Action(object):
    """An action consists of a single move."""
    def __init__(self):
        pass


    def perform(self, board):
        """Execute the action on the board."""
        pass


    def __str__(self):
        return str(type(self))



class AttackAction(Action):
    """Attack with a character."""
    def __init__(self, attacker=None, target=None):
        self.attacker = attacker
        self.target = target

    def perform(self, board):
        actions.minion_attack(board, self.attacker, self.target)


    def __str__(self):
        return "Use %s to attack %s" % (self.attacker.name, self.target.name)



class PlayMinionAction(Action):
    """Play a card to."""
    def __init__(self, minionCard=None, side=None, targetPos=None):
        self.minionCard = minionCard
        self.side = side
        self.targetPos = targetPos

    def perform(self, board):
        actions.play_minion_card(board, self.minionCard, self.targetPos)


    def __str__(self):
        return "Play minion %s on position %d" % (self.minionCard.name, self.targetPos)



class PlaySpellAction(Action):
    """Play a spell card."""
    def __init__(self, spellCard=None, target=None):
        self.spellCard = spellCard
        self.target = target

    def perform(self, board):
        actions.play_spell_card(board, self.spellCard, self.target)        


    def __str__(self):
        return "Play spell %s." % (self.spellCard.name)



class DoNothingAction(Action):
    """Don't do anything this action."""
    def perform(self, board):
        board.set_text("AI does nothing.")
        pass

    def __str__(self):
        return "Do nothing."
