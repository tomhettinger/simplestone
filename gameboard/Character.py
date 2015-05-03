class Character(object):
    """Base character class.
    """
    def __init__(self, name="Default", baseAttack=3, baseHealth=2, manaCost=2, status=None):
        self.name = name
        self.baseHealth = baseHealth
        self.currentHealth = baseHealth
        self.baseAttack = baseAttack
        self.currentAttack = baseAttack
        self.manaCost = manaCost
        self.attacksRemaining = 0
        self.targets = ['enemy', 'minion', 'hero']
        self.targetedBy = ['enemy', 'minion', 'hero', 'friendly', 'self']
        self.status = []
        if status is not None:
            if isinstance(status, basestring):
                self.status.append(status)
            else:
                self.status.extend(status)
        self.side = None
        self.board = None

    def __str__(self):
        out = "(%d  %s  %d)" % (self.currentAttack, self.name, self.currentHealth)
        if self.can_attack():
            out = "*" + out
        return out


    def deathrattle(self):
        self.board.outputText = "%s destroyed. DEATHRATTLE." % self.name
        # Execute deathrattle here.

    def battlecry(self):
        self.board.outputText = "%s is played from the hand. BATTLECRY." % self.name
        # Execute battlecry here.

    def can_attack(self):
        return (self.attacksRemaining > 0) and ('frozen' not in self.status) and (self.currentAttack > 0) and (self.side == self.board.playerTurn)


    def set_target_type(self, targetType):
        """Add a target type to this character's targetable types."""
        self.targets.append(targetType)


    def set_targetedBy_type(self, targetType):
        """Add a target type to this character's targeted by types."""
        self.targetedBy.append(targetType)


    def can_target(self, potentialTarget):
        """Return boolean for whether this character can target another character based 
        the targets attributes."""
        if isinstance(potentialTarget, Hero) and 'hero' not in self.targets:
            return False
        if isinstance(potentialTarget, Minion) and 'minion' not in self.targets:
            return False
        if potentialTarget.side != self.side and 'enemy' not in self.targets:
            return False
        if potentialTarget.side == self.side and 'friendly' not in self.targets:
            return False
        if potentialTarget is self and 'self' not in self.targets:
            return False
        return True


    def targetable_by(self, potentialAttacker):
        """Return boolean for whether this character can be targeted by another character based 
        the targets attributes."""
        if isinstance(potentialAttacker, Hero) and 'hero' not in self.targetedBy:
            return False
        if isinstance(potentialAttacker, Minion) and 'minion' not in self.targetedBy:
            return False
        if potentialAttacker.side != self.side and 'enemy' not in self.targetedBy:
            return False
        if potentialAttacker.side == self.side and 'friendly' not in self.targetedBy:
            return False
        if potentialAttacker is self and 'self' not in self.targetedBy:
            return False
        return True


    def add_status(self, status):
        self.status.append(status)


class Minion(Character):
    """Minion class inherits character class."""



class Hero(Character):
    """Hero class inherits character class."""
    def __init__(self, name="Default Hero", baseAttack=0, baseHealth=30, manaCost=0):
        super(Hero, self).__init__(name, baseAttack, baseHealth, manaCost)
        self.fatigueDMG = 1

    def __str__(self):
        out = "[%d  %s  %d]" % (self.currentAttack, self.name, self.currentHealth)
        if self.can_attack():
            out = "*" + out
        return out
