from copy import deepcopy
from random import random, shuffle
import threading

import Action

MAX_ACTION_LOOKAHEAD = 4

def create_child(parent, idx):
    """Create a DecisionTree.  This can be run as a thread."""
    boardCopy = deepcopy(parent.currentBoardState)
    action = boardCopy.get_available_actions()[idx]
    parent.children[idx] = DecisionTree(boardCopy, action, parent.level+1, parent, strategy=parent.strategy)



class DecisionTree(object):
    """A tree for deciding the best path of actions to take.  Strategy is a function that accepts
    a copy of the boardState and expects either a numeric value for winStrength (greater is better) or
    "force" or "avoid"."""
    def __init__(self, boardState, action=None, level=0, parent=None, strategy=None):
        self.currentBoardState = boardState
        self.action = action
        if level >= 20:
            raise Exception("20 consecutive actions is too many for one turn.")
        self.level = level
        self.parent = parent
        self.children = None
        self.winStrength = None
        self.maxWinStrength = None   # best winStrength if you choose this path.
        self.bestChild = None
        self.bestAction = None
        self.strategy = strategy

        # Perform initial action.        
        if self.action is not None:
            self.action.perform(self.currentBoardState)  # This will crash if a hero dies.
        # Calculate current win strength
        self.calculate_my_win_strength()
        # Find all possible moves.
        self.availableActions = self.currentBoardState.get_available_actions()
        # Create children
        self.create_children()
        # Calculate max win strength
        self.calculate_max_win_strength()
        # Calculate the best action from here.
        self.calculate_best_action()
        # Delete children to save RAM
        del self.children


    def get_winStrength(self):
        """Return the win strength value (calculate it if needed)."""
        if self.winStrength is None:
            self.calculate_my_win_strength()
        return self.winStrength


    def get_max_win_strength(self):
        """Return the maximum win strength of all leafs in this tree.
        Calculate it if necessary."""
        if self.maxWinStrength is None:
            self.calculate_max_win_strength()
        return self.maxWinStrength


    def get_best_child(self):
        """Return bestChild.  Calculate it if necessary."""
        if self.bestChild is None:
            self.calculate_best_child()
        return self.bestChild


    def get_best_action(self):
        """Return bestAction.  Calculate it if necessary."""
        if self.bestAction is None:
            self.calculate_best_action()
        return self.bestAction


    def create_children(self):
        """For each Action in the availableActions, create a decision tree with a hardcopy
        of the board state. If we just 'did nothing', don't make children."""
        # If action is to stop early, don't create children.
        if isinstance(self.action, Action.DoNothingAction):
            self.children = []
            return
        # If this is the (e.g. 4th) action, stop looking ahead.  CPU can't handle it.
        if self.level >= MAX_ACTION_LOOKAHEAD:
            self.children = []
            return
        actionCount = len(self.availableActions)
        self.children = [None] * actionCount

        # Split creation into multiple threads if this is the master node.
        if self.level == 0:
            threads = [None] * actionCount
            for idx in range(actionCount):
                threads[idx] = threading.Thread(target=create_child, args=(self, idx))
                threads[idx].start()
            for t in threads:
                t.join()
        else:
            for idx in range(actionCount):
                create_child(self, idx)


    def calculate_my_win_strength(self):
        """Calculate the strength of this boardState and return a value."""
        self.winStrength = self.strategy(deepcopy(self.currentBoardState))


    def calculate_max_win_strength(self):
        """Calculate the maximum win strength of all paths from here down to the roots."""
        if not len(self.children):
            self.maxWinStrength = self.get_winStrength()
        else:
            maxStrength = max([child.get_max_win_strength() for child in self.children])
            self.maxWinStrength = maxStrength


    def calculate_best_child(self):
        """Return the child that maximizes the chance of winning (it has the greatest maxWinStrength value)."""
        if not len(self.children):
            raise Exception("No actions can be done.")
        # Get a list of (child, maxWinStrength) tuples.  Then sort it.
        childValueTupleList = [(child, child.get_max_win_strength()) for child in self.children]
        childValueTupleList.sort(reverse=True, key=lambda tup: tup[1])
        # Find all children with wStrength equal to the best, then shuffle them to choose a random choice.
        equalButBestTup = [tup for tup in childValueTupleList if tup[1] == childValueTupleList[0][1]]
        shuffle(equalButBestTup)
        bestChild = equalButBestTup[0][0]
        self.bestChild = bestChild


    def calculate_best_action(self):
        """Set the bestAction attribute to an Action that represent the best thing to do."""
        if isinstance(self.action, Action.DoNothingAction):
            return
        if len(self.children):
            bestChild = self.get_best_child()
            idx = self.children.index(bestChild)
            self.bestAction = self.availableActions[idx]


    def print_tree(self):
        """Print this tree and all of the children.
        Can not be used if the children have been deleted to save RAM."""
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