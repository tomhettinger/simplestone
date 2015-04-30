#!/usr/bin/env python
from copy import deepcopy
import os, sys

from Character import Character
from Weapon import Weapon
from Spell import Spell
from Hand import Hand
from Card import Card
from Board import Board
import decks
import library
import actions


ACTION_CHOICES = ['p', 'a', 'h', 'e', 'q']


def refresh(board):
    os.system('clear')
    print board

def create_game():
    # Create the board
    board = Board()

    # Create the Heros and add to the board
    board.set_hero(library.create_character('rexar'), 'top')
    board.set_hero(library.create_character('anduin'), 'bottom')

    # Add minions to the board
    board.set_minion(library.create_character('boar'), 'top', 0)
    board.set_minion(library.create_character('boar'), 'top', 2)
    board.set_minion(library.create_character('raptor'), 'bottom', 1)
    board.set_minion(library.create_character('raptor'), 'bottom', 3)

    # Create player decks and shuffle them
    board.set_deck(decks.create_deck('basic'), 'top')
    board.set_deck(decks.create_deck('basic'), 'bottom')
    board.decks['top'].shuffle()
    board.decks['bottom'].shuffle()

    # Create the players hands
    board.set_hand(Hand(), 'top')
    board.set_hand(Hand(), 'bottom')

    # Draw three cards
    for i in range(3):
        actions.draw_card(board.decks['top'], board.hands['top'])
        actions.draw_card(board.decks['bottom'], board.hands['bottom'])

    return board


def play_character_from_hand(board, cardToPlay):
    while True:
        # Check if there is room to place the minion.
        side = board.playerTurn
        minions = board.minions[side]
        #if None not in board.minions[side]:

        playablePos = []
        for i, minion in enumerate(minions):
            if minion is None:
                playablePos.append(i)
        if not len(playablePos):
            board.outputText = "Not enough room for more minions."
            break

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
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            idx = int(command) - 1
            minion = cardToPlay.contents
            minion.board = board
            minion.battlecry()
            board.set_minion(minion, side, idx)
            board.hands[side].remove_card(cardToPlay)
            board.manaCurrent[side] -= minion.manaCost
            break


def play_weapon_from_hand():
    pass


def play_spell_from_hand():
    pass


def play_card(board):
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
                play_spell_from_hand()
            elif isinstance(cardToPlay.contents, Weapon):
                play_weapon_from_hand()
            else:
                raise Exception('Invalid card type.')
            break


def attack(board):
    while True:
        side = board.playerTurn
        chars = board.minions[side]
        chars.append(board.heroes[side])

        playableChars = []
        for i, char in enumerate(chars):
            if char is None:
                continue
            if char.can_attack():
                playableChars.append(i)
        if not len(playableChars):
            board.outputText = "No characters can attack."
            break

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

        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            idx = int(command) - 1
            attacker = chars[idx]
            defender = select_target(board)
            if defender is None:
                break
            actions.minion_attack(board, attacker, defender)
            break


def select_target(board):
    while True:
        if board.playerTurn == 'top':
            side = 'bottom'
        else:
            side = 'top'

        chars = board.minions[side]
        chars.append(board.heroes[side])

        attackableChars = []
        for i, char in enumerate(chars):
            if char is None:
                continue
            attackableChars.append(i)
        if not len(attackableChars):
            board.outputText = "No characters to attack."
            return None

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
    board.outputText = ""
    board.turnCount += 1
    if board.playerTurn == 'top':
        side = 'bottom'
    else:
        side = 'top'
    board.playerTurn = side
    board.manaBase[side] += 1
    board.manaCurrent[side] = board.manaBase[side]
    actions.draw_card(board.decks[side], board.hands[side])


def main():
    board = create_game()
    refresh(board)
    #actions.minion_attack(board, board.minions['bottom'][1], board.minions['top'][2])
    #actions.play_minion(board, 'bottom', board.hands['bottom'].cards.pop(3), pos=2)
    #print board
    #actions.minion_attack(board, board.minions['bottom'][3], board.heroes['top'])
    #print board

    while True:
        command = ''
        while command not in ACTION_CHOICES:
            refresh(board)    
            command = raw_input("{:^100}".format("[p] Play Card   [a] Attack w/ Char   [h] Hero Power   [e] End Turn   [q] Quit\n"))
        if command == 'q':
            sys.exit()
        elif command == 'p':
            play_card(board)
	    continue
        elif command == 'a':
            attack(board)
	    continue
        elif command == 'h':
	    continue
        elif command == 'e':
	    advance_turn(board)


if __name__ == "__main__":
    main()
