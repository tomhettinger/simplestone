"""Runs the main game loop and user interface.
"""
import os, sys
from copy import copy, deepcopy

import actions
from Character import Character
from Character import Character
from Weapon import Weapon
from Spell import Spell

EMPTY_LINE = '{}{:>141}'.format('#', '#\n')
BORDER_LINE = "{:#>142}".format("\n")


def enemy(side):
    """Return the side opposite of the given side."""
    if side == 'top':
        return 'bottom'
    elif side == 'bottom':
        return 'top'
    else:
        raise Exception('Invalid side: %s' % side)


def refresh(board):
    """Clear the board and redraw it."""
    os.system('clear')
    #print board

    # Border
    out = "\n"
    out += BORDER_LINE

    # Hand, Deck and Mana 
    deckOut = "Deck: %d   " % board.decks['top'].size
    manaOut = "Mana: {%d/%d}" % (board.manaCurrent['top'], board.manaBase['top'])
    out += "{}{:>137}{}".format('# ', deckOut+manaOut, ' #\n')
    handOut = str(board.hands['top'])
    out += "{}{:<137}{}".format('# ', handOut, ' #\n')
    out += EMPTY_LINE
    out += EMPTY_LINE

    # Hero
    if board.heroes['top'] is None:
        out += "{}{:^137}{}".format('# ', "None", ' #\n')
    else:
        out += "{}{:^137}{}".format('# ', str(board.heroes['top']), ' #\n')
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE

    # Minions
    minionOut = []
    for m in board.minions['top']:
        if m is None:
            minionOut.append("____")
        else:
            minionOut.append(str(m))
    minOut = ['# ',]
    minOut.extend(minionOut)
    minOut.extend([' #\n'])
    out += "{:<4}{:^19}{:^19}{:^19}{:^19}{:^19}{:^19}{:^19}{:>5}".format(*minOut)
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE
    minionOut = []
    for m in board.minions['bottom']:
        if m is None:
            minionOut.append("____")
        else:
            minionOut.append(str(m))
    minOut = ['# ',]
    minOut.extend(minionOut)
    minOut.extend([' #\n'])
    out += "{:<4}{:^19}{:^19}{:^19}{:^19}{:^19}{:^19}{:^19}{:>5}".format(*minOut)
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE
    out += EMPTY_LINE

    # Hero
    if board.heroes['bottom'] is None:
        out += "{}{:^137}{}".format('#', "None", ' #\n')
    else:
        out += "{}{:^137}{}".format('# ', str(board.heroes['bottom']), ' #\n')
    out += EMPTY_LINE
    out += EMPTY_LINE

    # Hand, Deck and Mana 
    handOut = str(board.hands['bottom'])
    out += "{}{:<137}{}".format('# ', handOut, ' #\n')
    deckOut = "Deck: %d   " % board.decks['bottom'].size
    manaOut = "Mana: {%d/%d}" % (board.manaCurrent['bottom'], board.manaBase['bottom'])
    out += "{}{:>137}{}".format('# ', deckOut+manaOut, ' #\n')

    # Border
    out += BORDER_LINE
    out += "{:<140}".format(board.get_text())
    out += "\n"

    print out


def check_if_game_over(board):
    """End the game if a hero is dead."""
    if (board.get_hero(side='top').currentHealth <= 0):
        print "\n\nBottom player wins.  Thank you for playing."
        sys.exit()
    elif (board.get_hero(side='bottom').currentHealth <= 0):
        print "\n\nTop player wins.  Thank you for playing."
        sys.exit()


def play_loop(board, ai=None):
    """The highest level of the loop.  Allow player to decide what actions to take, or end the turn."""
    while True:
        refresh(board)
        check_if_game_over(board)

        # If enemy turn, let the AI play.
        if board.get_side() == "top" and ai is not None:
            board.set_text("AI turn.")
            ai.play_turn()
            continue

        # Ask for instructions
        command = None
        while command not in ['p', 'a', 'h', 'e', 'q']:
            refresh(board)  
            command = raw_input("{:^100}".format("[p] Play Card   [a] Attack w/ Char   [h] Hero Power   [e] End Turn   [q] Quit\n"))

        # Execute insructions
        if command == 'q':
            sys.exit()
        elif command == 'p':
            play_card(board)
            continue
        elif command == 'a':
            select_attacker(board)
            continue
        elif command == 'h':
            continue
        elif command == 'e':
            end_turn(board)
            continue


def play_card(board):
    """Spend mana to play a card."""
    while True:
        hand = board.get_hand()

        # Check if there are any cards to play.
        playableCardPos = hand.get_playable_card_positions()
        if not len(playableCardPos):
            board.set_text("No cards to play.")
            break

        # Give options and request instructions
        play_choices = ['b', 'q']
        play_choices.extend([str(x) for x in playableCardPos])
        command = None
        while command not in play_choices:
            board.set_text("Select a card:")
            refresh(board)
            outLine = ""
            for i in playableCardPos:
                outLine += "<%d> %s   " % (i, hand.cards[i-1].name)
            outLine += "<b> Back   <q> Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instruction
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            pos = int(command)
            cardToPlay = hand.get_card(pos)
            board.set_text('Playing %s' % cardToPlay.name)
            if isinstance(cardToPlay.contents, Character):
                play_character_from_hand(board, cardToPlay)
            elif isinstance(cardToPlay.contents, Spell):
                play_spell_from_hand(board, cardToPlay)
            elif isinstance(cardToPlay.contents, Weapon):
                play_weapon_from_hand(board, cardToPlay)
            else:
                raise Exception('Invalid card type.')
            break


def play_character_from_hand(board, cardToPlay):
    while True:
        """Try to play a minion from the hand.  Doing so causes a battlecry."""
        # Check if there is room to place the minion.        
        emptyMinionPos = board.get_empty_minion_positions()
        if not len(emptyMinionPos):
            board.set_text("Not enough room for more minions.")
            break

        # Give the available positions to drop minion and request instructions.
        play_choices = ['b', 'q']
        play_choices.extend([str(x) for x in emptyMinionPos])
        command = None
        while command not in play_choices:
            board.set_text("Select a position to place minion:")
            refresh(board)
            outLine = ""
            for i in emptyMinionPos:
                outLine += "<%d>   " % i
            outLine += "<b> Back   <q> Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instructions
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            pos = int(command)
            minion = cardToPlay.contents
            # Place minion, excecute the battlecry, remove attack, remove from hand, reduce player mana.
            minion.board = board
            minion.battlecry()
            board.subtract_mana(minion.manaCost)
            board.get_hand().remove_card(cardToPlay)
            board.summon_minion(minion, board.get_side(), pos)
            break


def play_weapon_from_hand(board, cardToPlay):
    """Equip a weapon."""
    side = board.playerTurn
    weapon = cardToPlay.contents
    # Equip Weapon
    board.set_text("Equipping %s. (Not implemented yet)." % weapon.name)
    # Remove from hand and reduce players mana.
    board.hands[side].remove_card(cardToPlay)
    board.manaCurrent[side] -= weapon.manaCost


def play_spell_from_hand(board, cardToPlay):
    """Cast a spell."""
    spell = cardToPlay.contents
    # Cast spell
    board.set_text("Casting %s. (Not implemented yet, except The Coin)." % spell.name)
    if spell.name == 'The Coin':
        board.add_mana(1)
    # Remove from hand and reduce players mana.
    board.subtract_mana(spell.manaCost)
    board.get_hand().remove_card(cardToPlay)
    

def select_attacker(board):
    """Select a minion to use to do some attacking.  If valid attacker and defender are choosen,
    perform the attack."""
    while True:
        # Check if there are any characters that can attack.
        canAttackPos = board.get_canAttack_char_positions()
        if not len(canAttackPos):
            board.set_text("No characters can attack.")
            break

        # Give options for attacker and ask for instructions.
        play_choices = ['b', 'q']
        play_choices.extend([str(x) for x in canAttackPos])
        command = None
        while command not in play_choices:
            board.set_text("Select a character to attack with:")
            refresh(board)
            outLine = ""
            for i in canAttackPos:
                outLine += "<%d> %s   " % (i, board.get_character(i).name)
            outLine += "<b> Back   [q] Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instructions
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            pos = int(command)
            attacker = board.get_character(pos)
            defender = select_target(board, attacker)
            if defender is None:
                break
            actions.minion_attack(board, attacker, defender)
            break


def select_target(board, attacker):
    """Currently, a player can only attack an enemy.  To change this, check the attackers targeting
    powers and cross-check that with every characters side attribute."""
    while True:
        # Check if there are any enemies to attack.
        attackableCharacters = board.get_targetable_characters(attacker)
        for character in attackableCharacters:
            print character.name
        if not len(attackableCharacters):
            board.set_text("No characters to attack.")
            return None
        attackableCharacters.sort(key=lambda char: int(board.get_target_pos(char)))

        # Give available choices and ask for instructions.
        play_choices = ['b', 'q']
        for char in attackableCharacters:
            play_choices.append(str(board.get_target_pos(char)))
        command = None
        while command not in play_choices:
            board.set_text("Select an enemy to attack:")
            refresh(board)
            outLine = ""
            for char in attackableCharacters:
                pos = board.get_target_pos(char)
                outLine += "<%d> %s   " % (pos, char.name)
            outLine += "<b> Back   <q> Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instructions.
        if command == 'q':
            sys.exit()
        elif command == 'b':
            return None
        else:
            pos = int(command)
            target = board.get_character_by_position(pos)
            return target


def end_turn(board):
    """End the turn and take necessary actions."""
    # Do stuff here, like end of turn effects.
    # Check if either hero is dead.
    check_if_game_over(board)
    begin_turn(board)


def begin_turn(board):
    """Begin the turn and take necessary actions."""
    # Increase counter and switch sides.
    board.set_text("")
    board.increment_turn()
    board.change_side()

    # Add mana crystal and reset mana count to full.
    board.update_mana()

    # Reset the attacks of characters on this side.
    board.reset_attacksRemaining()

    # Draw a card.
    actions.draw_card(board, board.get_side())
