from Character import Hero, Minion
from Weapon import Weapon
from Spell import Spell

# Heros
rexar = Hero("Rexar", 0, 30)
anduin = Hero("Anduin", 0, 30)

# Minions
boar = Minion("Boar", 1, 1, 1)
raptor = Minion("Raptor", 2, 3, 2)
coreHound = Minion("Core Hound", 9, 5, 7)

# Weapons
axe = Weapon("Axe", 4, 1, 3)

# Spells
fireball = Spell("Fireball", 4)
fireball.set_effect(spellType="DealDmg", target="anyEnemeyMinion", value=6)
