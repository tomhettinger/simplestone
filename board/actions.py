"""Set of actions that can happen.
"""

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


def draw_card(board, side):
    """Draw the top card from the deck and place it into the hand."""
    deck = board.decks[side]
    hand = board.hands[side]
    cardDrawn = deck.draw_card()

    # If deck is empty, deal fatigue damage.
    if cardDrawn is None:
        deal_fatigue(board.heroes[side])
        return

    if hand.is_full():
        board.outputText = "Hand is full, burning:  %s" % cardDrawn.contents.name
    else:
        hand.add_card(cardDrawn)


def play_minion(board, side, character, pos):
    """Play a minion from your hand onto the field."""
    minions = board.minions[side]
    if character.manaCost > board.manaCurrent[side]:
        raise Exception("Not enough mana. %d > %d" % (character.manaCost, board.manaCurrent[side]))
    if minions[pos] is not None:
        raise Exception("%s already on this spot." % minions[pos].name)
    board.manaCurrent[side] -= character.manaCost
    board.summon_minion(character, side, pos)
    character.battlecry()


def deal_fatigue(hero):
    """Deal fatigue damage to a hero."""
    # Deal the damage, then increase the fatigue counter.
    hero.currentHealth -= hero.fatigueDMG
    hero.board.outputText = "Hero takes %d fatigue damage." % hero.fatigueDMG
    hero.fatigueDMG += 1


def deal_damage(board, side, pos, damage):
    """Deal some damage to a minion on the board."""
    pass
