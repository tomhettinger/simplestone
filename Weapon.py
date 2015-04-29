class Weapon(object):
    def __init__(self, name="Default Weapon", baseAttack=2, baseDurability=2, manaCost=0):
        self.name = name
        self.baseAttack = baseAttack
        self.currentAttack = baseAttack
        self.baseDurability = baseDurability
        self.currentDurability = baseDurability
        self.manaCost = manaCost
