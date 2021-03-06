class Spell(object):
    def __init__(self, name="Default Spell", manaCost=0, spellType=None):
        self.name = name
        self.manaCost = manaCost
        self.spellType = spellType


    def set_effect(self, **kwargs):
        if "spellType" in kwargs:
            self.spellType = kwargs["spellType"]
        if "target" in kwargs:
            self.target = kwargs["target"]
        if "value" in kwargs:
            self.value = kwargs["value"]


    def cast(self, board, target=None):
        """Temporary cast method."""
        board.set_text("Casting %s. (Not implemented yet, except The Coin)." % self.name)
        if self.name == "The Coin":
            board.add_mana(1)