"""Set of actions that can happen.
"""

def minion_attack(board, attacker, defender):
    """Attack the defender with attacker."""
    board.set_text("%s attacks %s." % (attacker.name, defender.name))
    defender.take_damage(attacker.currentAttack)
    attacker.take_damage(defender.currentAttack)
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
        board.set_text("Hand is full, burning:  %s" % cardDrawn.contents.name)
    else:
        hand.add_card(cardDrawn)


def play_minion_card(board, card, pos):
    """Play a minion from a hand onto the field."""
    #minions = board.get_minions(side)
    side = board.get_side()
    minion = card.contents
    if minion.manaCost > board.manaCurrent[side]:
        raise Exception("Not enough mana. %d > %d" % (minion.manaCost, board.manaCurrent[side]))
    minion.board = board
    minion.battlecry()
    board.subtract_mana(minion.manaCost)
    board.get_hand().remove_card(card)
    board.summon_minion(minion, side, pos)


def play_spell_card(board, card, target=None):
    """Play a spell card.  Cast the spell, subtract mana, and throw away card."""
    spell = card.contents
    board.subtract_mana(spell.manaCost)
    board.get_hand().remove_card(card)
    spell.cast(board, target)


def deal_fatigue(hero):
    """Deal fatigue damage to a hero."""
    # Deal the damage, then increase the fatigue counter.
    hero.currentHealth -= hero.fatigueDMG
    hero.board.set_text("Hero takes %d fatigue damage." % hero.fatigueDMG)
    hero.fatigueDMG += 1


def deal_damage(board, side, pos, damage):
    """Deal some damage to a minion on the board."""
    pass
