class Character(object):
    """Base character class.
    """
    def __init__(self, name="Default", baseAttack=3, baseHealth=2, manaCost=2):
	self.name = name
        self.baseHealth = baseHealth
        self.currentHealth = baseHealth
        self.baseAttack = baseAttack
        self.currentAttack = baseAttack
        self.manaCost = manaCost
	self.attacksRemaining = 1
        self.status = []
        self.side = None
	self.board = None

    def __str__(self):
        out = "(%d  %s  %d)" % (self.currentAttack, self.name, self.currentHealth)
        if self.can_attack():
            out = "*" + out
        return out


    def deathrattle(self):
        print "%s destroyed. DEATHRATTLE." % self.name


    def battlecry(self):
        print "%s is played from the hand. BATTLECRY." % self.name


    def can_attack(self):
        return (self.attacksRemaining > 0) and ('frozen' not in self.status) and (self.currentAttack > 0) and (self.side == self.board.playerTurn)



class Minion(Character):
    """Minion class inherits character class."""



class Hero(Character):
    """Hero class inherits character class."""
    def __init__(self, name="Default Hero", baseAttack=0, baseHealth=30, manaCost=0):
        super(Hero, self).__init__(name, baseAttack, baseHealth, manaCost)
