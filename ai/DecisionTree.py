from copy import deepcopy
from random import random

class DecisionTree(object):
    """A tree for deciding the best path of actions to take."""
    def __init__(self, boardState, action=None, level=0, parent=None):
        self.currentBoardState = boardState
        self.action = action
        if level >= 100:
            raise Exception("100 consecutive actions is too many for one turn.")
        self.level = level
        self.parent = parent
        self.children = []
        self.winStrength = None
        self.maxWinStrength = None   # best winStrength if you choose this path.

        # Perform initial action.        
        if self.action is not None:
            self.action.perform(self.currentBoardState)  # This will crash if a hero dies.
        # Calculate current win strength
        self.calculate_win_strength()
        # Find all possible moves.
        self.availableActions = self.currentBoardState.get_available_actions()  # This should be copied over from the AI class method.
        # Create children
        self.create_children()


    def get_winStrength(self):
        """Return the win strength value (calculate it if needed)."""
        if self.winStrength is None:
            self.calculate_win_strength()
        return self.winStrength


    def create_children(self):
        """For each Action in the availableActions, create a decision tree with a hardcopy
        of the board state."""
        for action in self.availableActions:
            child = DecisionTree(deepcopy(self.currentBoardState), action, self.level+1, self)
            self.children.append(child)


    def calculate_win_strength(self):
        """Calculate the strength of this boardState and return a value."""
        self.winStrength = random()   # Temporary place holder.


    def calculate_max_win_strength(self):
        """Calculate the maximum win strength of all leafs in this tree."""
        if not len(self.children):
            self.maxWinStrength = self.get_winStrength()
        else:
            maxStrength = max([child.get_max_win_strength() for child in children])
            self.maxWinStrength = maxStrength


    def get_max_win_strength(self):
        """Return the maximum win strength of all leafs in this tree.
        Calculate it if necessary."""
        if self.maxWinStrength is not None:
            self.calculate_max_win_strength()
        return self.maxWinStrength


    def get_best_child(self):
        """Return the child that maximizes the chance of winning (it has the greatest maxWinStrength value)."""
        if not len(self.children):
            raise Exception("No actions can be done.")
        # Get a list of (child, maxWinStrength) tuples.  Then sort it.
        childValueTupleList = [(child, child.get_max_win_strength()) for child in self.children]
        childValueTupleList.sort(reverse=True, key=lambda tup: tup[1])
        bestChild = childValueTupleList[0][0]
        return bestChild


    #def calculate_best_action_list(self):
    #    """Return a list of actions that represent the best course of action."""
    #    actionList = []
    #    if not len(self.children):
    #        return actionList
    #    actionList.append()