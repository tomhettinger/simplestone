"""Runs the main game loop and user interface.
"""
import os, sys
from copy import copy, deepcopy

import actions
from Character import Character
from Character import Character
from Weapon import Weapon
from Spell import Spell


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
    print board


def play_loop(board):
    """The highest level of the loop.  Allow player to decide what actions to take, or end the turn."""
    while True:
        refresh(board)

        # Check if either hero is dead.
        if (board.heroes['top'].currentHealth <= 0):
            print "\n\nBottom player wins.  Thank you for playing."
            sys.exit()
        elif (board.heroes['top'].currentHealth <= 0):
            print "\n\nTop player wins.  Thank you for playing."
            sys.exit()

        command = ''
        while command not in ['p', 'a', 'h', 'e', 'q']:
            refresh(board)  
            command = raw_input("{:^100}".format("[p] Play Card   [a] Attack w/ Char   [h] Hero Power   [e] End Turn   [q] Quit\n"))
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
            advance_turn(board)


def play_card(board):
    """Spend mana to play a card."""
    while True:
        hand = board.hands[board.playerTurn]

        # Check if there are any cards to play.
        playableCards = []
        for i, card in enumerate(hand.cards):
            if card.can_play():
                 playableCards.append(i)
        if not len(playableCards):
            board.outputText = "No cards to play."
            break

        # Give options and request instructions
        play_choices = ['b', 'q']
        play_choices.extend([str(x+1) for x in playableCards])
        command = ''
        while command not in play_choices:
            board.outputText = "Select a card:"
            refresh(board)
            outLine = ""
            for i in playableCards:
                outLine += "[%d] %s   " % ((i+1), hand.cards[i].name)
            outLine += "[b] Back   [q] Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instruction
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            idx = int(command) - 1
            cardToPlay = hand.cards[idx]
            board.outputText = 'Playing %s' % cardToPlay.name
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
        side = board.playerTurn
        minions = copy(board.minions[side])
        playablePos = []
        for i, minion in enumerate(minions):
            if minion is None:
                playablePos.append(i)
        if not len(playablePos):
            board.outputText = "Not enough room for more minions."
            break

        # Give the available positions to drop minion and request instructions.
        play_choices = ['b', 'q']
        play_choices.extend([str(x+1) for x in playablePos])
        command = ''
        while command not in play_choices:
            board.outputText = "Select a position to place minion:"
            refresh(board)
            outLine = ""
            for i in playablePos:
                outLine += "[%d]   " % (i+1)
            outLine += "[b] Back   [q] Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instructions
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            idx = int(command) - 1
            minion = cardToPlay.contents
            # Place minion, excecute the battlecry, remove attack, remove from hand, reduce player mana.
            minion.board = board
            minion.battlecry()
            if "charge" not in minion.status:
                minion.attacksRemaining = 0
            print minion.status
            board.set_minion(minion, side, idx)
            board.hands[side].remove_card(cardToPlay)
            board.manaCurrent[side] -= minion.manaCost
            break


def play_weapon_from_hand(board, cardToPlay):
    """Equip a weapon."""
    side = board.playerTurn
    weapon = cardToPlay.contents
    # Equip Weapon
    board.outputText = "Equipping %s. (Not implemented yet)." % weapon.name
    # Remove from hand and reduce players mana.
    board.hands[side].remove_card(cardToPlay)
    board.manaCurrent[side] -= weapon.manaCost


def play_spell_from_hand(board, cardToPlay):
    """Cast a spell."""
    side = board.playerTurn
    spell = cardToPlay.contents
    # Cast spell
    board.outputText = "Casting %s. (Not implemented yet)." % spell.name
    # Remove from hand and reduce players mana.
    board.hands[side].remove_card(cardToPlay)
    board.manaCurrent[side] -= spell.manaCost


def select_attacker(board):
    """Select a minion to use to do some attacking.  If valid attacker and defender are choosen,
    perform the attack."""
    while True:
        side = board.playerTurn
        chars = copy(board.minions[side])
        chars.append(board.heroes[side])

        # Check if there are any characters that can attack.
        playableChars = []
        for i, char in enumerate(chars):
            if char is None:
                continue
            if char.can_attack():
                playableChars.append(i)
        if not len(playableChars):
            board.outputText = "No characters can attack."
            break

        # Give options for attacker and ask for instructions.
        play_choices = ['b', 'q']
        play_choices.extend([str(x+1) for x in playableChars])
        command = ''
        while command not in play_choices:
            board.outputText = "Select a character to attack with:"
            refresh(board)
            outLine = ""
            for i in playableChars:
                outLine += "[%d] %s   " % ((i+1), chars[i].name)
            outLine += "[b] Back   [q] Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instructions
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            idx = int(command) - 1
            attacker = chars[idx]
            defender = select_target(board, attacker)
            if defender is None:
                break
            actions.minion_attack(board, attacker, defender)
            break


def select_target(board, attacker):
    """Currently, a player can only attack an enemy.  To change this, check the attackers targeting
    powers and cross-check that with every characters side attribute."""
    while True:
        side = enemy(board.playerTurn)

        # Check if there are any enemies to attack.
        chars = copy(board.minions[side])
        chars.append(board.heroes[side])
        attackableChars = []
        for i, char in enumerate(chars):
            if char is None:
                continue
            attackableChars.append(i)
        if not len(attackableChars):
            board.outputText = "No characters to attack."
            return None

        # Give available choices and ask for instructions.
        play_choices = ['b', 'q']
        play_choices.extend([str(x+1) for x in attackableChars])
        command = ''
        while command not in play_choices:
            board.outputText = "Select an enemy to attack:"
            refresh(board)
            outLine = ""
            for i in attackableChars:
                outLine += "[%d] %s   " % ((i+1), chars[i].name)
            outLine += "[b] Back   [q] Quit\n"
            command = raw_input("{:^100}".format(outLine))

        # Execute instructions.
        if command == 'q':
            sys.exit()
        elif command == 'b':
            return None
        else:
            idx = int(command) - 1
            target = chars[idx]
            return target


def advance_turn(board):
    """Move to the next players turn."""
    # Increase counter and switch sides.
    board.outputText = ""
    board.turnCount += 1
    newSide = enemy(board.playerTurn)
    board.playerTurn = newSide

    # Add mana crystal and reset mana count to full.
    if board.manaBase[newSide] < 10:
        board.manaBase[newSide] += 1
    board.manaCurrent[newSide] = board.manaBase[newSide]

    # Draw a card.
    actions.draw_card(board, newSide)

    # Reset the attacks of characters on this side.
    for minion in board.minions[newSide]:
        if minion is None:
            continue
        minion.attacksRemaining = 1
        if 'windfury' in minion.status:
            minion.attacksRemaining += 1
    hero = board.heroes[newSide]
    hero.attacksRemaining = 1
    if 'windfury' in hero.status:
        hero.attacksRemaining += 1

