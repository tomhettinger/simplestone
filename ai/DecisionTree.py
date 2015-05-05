from copy import deepcopy
from random import random
import Action

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
        self.bestAction = None

        # Perform initial action.        
        if self.action is not None:
            self.action.perform(self.currentBoardState)  # This will crash if a hero dies.
        # Calculate current win strength
        self.calculate_win_strength()
        # Find all possible moves.
        self.availableActions = self.currentBoardState.get_available_actions()
        # Create children
        self.create_children()
        # Set the best action
        self.calculate_best_action()


    def get_winStrength(self):
        """Return the win strength value (calculate it if needed)."""
        if self.winStrength is None:
            self.calculate_win_strength()
        return self.winStrength


    def create_children(self):
        """For each Action in the availableActions, create a decision tree with a hardcopy
        of the board state. If we just 'did nothing', don't make children."""
        if isinstance(self.action, Action.DoNothingAction):
            return
        #if len(self.availableActions) == 1 and isinstance(self.availableActions[0], Action.DoNothingAction):
        #    return
        for a in range(len(self.availableActions)):
            boardCopy = deepcopy(self.currentBoardState)
            action = boardCopy.get_available_actions()[a]
            child = DecisionTree(boardCopy, action, self.level+1, self)
            self.children.append(child)


    def calculate_win_strength(self):
        """Calculate the strength of this boardState and return a value."""
        self.winStrength = random()   # Temporary place holder.


    def calculate_max_win_strength(self):
        """Calculate the maximum win strength of all leafs in this tree."""
        if not len(self.children):
            self.maxWinStrength = self.get_winStrength()
        else:
            maxStrength = max([child.get_max_win_strength() for child in self.children])
            self.maxWinStrength = maxStrength


    def get_max_win_strength(self):
        """Return the maximum win strength of all leafs in this tree.
        Calculate it if necessary."""
        if self.maxWinStrength is None:
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


    def calculate_best_action(self):
        """Set the bestAction attribute to an Action that represent the best thing to do."""
        if isinstance(self.action, Action.DoNothingAction):
            return
        if len(self.availableActions):
            bestChild = self.get_best_child()
            idx = self.children.index(bestChild)
            self.bestAction = self.availableActions[idx]


    def print_tree(self):
        """Print this tree and all of the children."""
        out = ""
        for i in range(self.level):
            out += '   |'
        out += '___'
        out += str(self.action)
        if self.action is None:
            print "None"
        else:
            print out
        for child in self.children:
            child.print_tree()