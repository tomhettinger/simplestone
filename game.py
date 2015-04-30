#!/usr/bin/env python
from copy import deepcopy
import os, sys

from Hand import Hand
from Card import Card
from Board import Board
import decks
import library
import actions

ACTION_CHOICES = ['p', 'a', 'h', 'e', 'q']
PLAY_CHOICES = ['1', '2', '3', '4', '5', 'b', 'q']

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
    #hand1.add_card(Card(deepcopy(library.boar)))
    #hand1.add_card(Card(deepcopy(library.fireball)))
    #hand1.add_card(Card(deepcopy(library.raptor)))
    #for i in range(3):
    #    hand1.cards[i].side = 'top'
    #    hand1.cards[i].board = board
    board.set_hand(Hand(), 'top')

    #hand2.add_card(Card(deepcopy(library.axe)))
    #hand2.add_card(Card(deepcopy(library.coreHound)))
    #hand2.add_card(Card(deepcopy(library.raptor)))
    #hand2.add_card(Card(deepcopy(library.boar)))
    #for i in range(4):
    #    hand2.cards[i].side = 'bottom'
    #    hand2.cards[i].board = board
    board.set_hand(Hand(), 'bottom')

    return board


def play_card(board):
    while True:
        hand = board.hands[board.playerTurn]
        command = ''
        while command not in PLAY_CHOICES:
            refresh(board)
            command = raw_input("{:^100}".format("[1]   [2]   [3]   [4]   [5]   [b] Back   [q] Quit\n"))
        if command == 'q':
            sys.exit()
        elif command == 'b':
            break
        else:
            print 'Playing card %s' % command
            break

def main():
    board = create_game()
    refresh(board)
    actions.minion_attack(board, board.minions['bottom'][1], board.minions['top'][2])
    #actions.play_minion(board, 'bottom', board.hands['bottom'].cards.pop(3), pos=2)
    #print board
    #actions.minion_attack(board, board.minions['bottom'][3], board.heroes['top'])
    #print board

    while True:
        command = ''
        while command not in ACTION_CHOICES:
            refresh(board)    
            command = raw_input("{:^100}".format("[p] Play Card   [a] Attack w/ Character   [h] Hero Power   [e] End Turn   [q] Quit\n"))
        if command == 'q':
            sys.exit()
        elif command == 'p':
            play_card(board)
	    continue
        elif command == 'a':
	    continue
        elif command == 'h':
	    continue
        elif command == 'e':
	    continue


if __name__ == "__main__":
    main()
