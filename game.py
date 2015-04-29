#!/usr/bin/env python
from copy import deepcopy
import os, sys

from Hand import Hand
from Board import Board
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
    board.set_topHero(deepcopy(library.rexar))
    board.set_bottomHero(deepcopy(library.anduin))

    # Add minions to the board
    board.set_minion(deepcopy(library.boar), "top", 0)
    board.set_minion(deepcopy(library.boar), "top", 2)
    board.set_minion(deepcopy(library.raptor), "bottom", 1)
    board.set_minion(deepcopy(library.boar), "bottom", 3)

    # Create the players hands
    hand1 = Hand()
    hand1.add_card(deepcopy(library.boar))
    hand1.add_card(deepcopy(library.fireball))
    hand1.add_card(deepcopy(library.raptor))
    hand2 = Hand()
    hand2.add_card(deepcopy(library.axe))
    hand2.add_card(deepcopy(library.coreHound))
    hand2.add_card(deepcopy(library.raptor))
    hand2.add_card(deepcopy(library.boar))

    # Add hands to the board
    board.set_topHand(hand1)
    board.set_bottomHand(hand2)

    return board

def play_card(board):
    while True:
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
