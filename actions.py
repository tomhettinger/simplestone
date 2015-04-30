"""Set of actions that can be done by the players (or other)."""

def minion_attack(board, attacker, defender):
    """Attack the defender with attacker."""
    board.outputText = "%s attacks %s." % (attacker.name, defender.name)
    defender.currentHealth -= attacker.currentAttack
    attacker.currentHealth -= defender.currentAttack
    attacker.attacksRemaining -= 1
    if defender.currentHealth <= 0:
        board.destroy_minion(defender)
    if attacker.currentHealth <= 0:
        board.destroy_minion(attacker)


def draw_card(deck, hand):
    """Draw the top card from the deck and place it into the hand."""
    cardDrawn = deck.draw_card()
    hand.add_card(cardDrawn)
    cardDrawn.hand = hand


def play_minion(board, side, character, pos):
    """Play a minion from your hand onto the field."""
    minions = board.minions[side]
    if character.manaCost > board.manaCurrent[side]:
        raise Exception("Not enough mana. %d > %d" % (character.manaCost, board.manaCurrent[side]))
    if minions[pos] is not None:
        raise Exception("%s already on this spot." % minions[pos].name)
    board.manaCurrent[side] -= character.manaCost
    board.set_minion(character, side, pos)
    character.battlecry()


def deal_damage(board, side, pos, damage):
    """Deal some damage to a minion on the board."""
    pass
